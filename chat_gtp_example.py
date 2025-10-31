import os, time, json, gzip, io, requests
from sp_api.api import Reports
from sp_api.base import SellingApiException

EU_ENDPOINT = "https://sellingpartnerapi-eu.amazon.com"
LWA_TOKEN_URL = "https://api.amazon.com/auth/o2/token"

def lwa_access_token():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.environ["LWA_REFRESH_TOKEN"],
        "client_id": os.environ["LWA_APP_ID"],
        "client_secret": os.environ["LWA_CLIENT_SECRET"],
    }
    r = requests.post(LWA_TOKEN_URL, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

def create_rdt(lwa_token, report_document_id):
    url = f"{EU_ENDPOINT}/tokens/2021-03-01/restrictedDataToken"
    payload = {
        "restrictedResources": [
            {
                "method": "GET",
                "path": f"/reports/2021-06-30/documents/{report_document_id}"
            }
        ]
    }
    r = requests.post(url, headers={
        "Content-Type": "application/json",
        "x-amz-access-token": lwa_token
    }, data=json.dumps(payload))
    r.raise_for_status()
    return r.json()["restrictedDataToken"]

def main():
    mkt_ids = os.environ["MARKETPLACE_IDS"].split(",")
    start_iso = "2025-07-01T00:00:00Z"
    end_iso   = "2025-07-31T23:59:59Z"

    reports = Reports()  # creds via env (LWA, AWS keys, role_arn, region)

    # 1) Create VAT Transaction report (no RDT needed)
    create = reports.create_report(
        reportType="GET_VAT_TRANSACTION_DATA",
        dataStartTime=start_iso,
        dataEndTime=end_iso,
        marketplaceIds=mkt_ids
    )
    report_id = create.payload["reportId"]
    print("Created:", report_id)

    # 2) Poll until DONE (no RDT)
    while True:
        status = reports.get_report(reportId=report_id).payload
        ps = status["processingStatus"]
        print("Status:", ps)
        if ps == "DONE":
            break
        if ps in ("CANCELLED","FATAL","DONE_NO_DATA"):
            raise RuntimeError(f"Report ended with {ps}")
        time.sleep(15)

    doc_id = status["reportDocumentId"]

    # 3) Get a normal LWA token, then request an RDT for getReportDocument
    lwa = lwa_access_token()
    rdt = create_rdt(lwa, doc_id)

    # 4) Call get_report_document WITH the RDT (SDK doesn’t expose RDT param directly,
    #    so call raw; or if your SDK version supports it, pass restricted_data_token)
    url = f"{EU_ENDPOINT}/reports/2021-06-30/documents/{doc_id}"
    meta = requests.get(url, headers={"x-amz-access-token": rdt})
    meta.raise_for_status()
    meta = meta.json()

    # 5) Download using the pre-signed URL (no auth)
    download = requests.get(meta["url"])
    download.raise_for_status()
    raw_bytes = download.content

    # Decompress if needed
    if meta.get("compressionAlgorithm","").upper() == "GZIP":
        with gzip.GzipFile(fileobj=io.BytesIO(raw_bytes)) as gz:
            raw_bytes = gz.read()

    # Save using a sensible extension
    out = "VAT_Transaction_Report.tsv"
    if "json" in meta.get("contentType","").lower(): out = "VAT_Transaction_Report.json"
    with open(out, "wb") as f:
        f.write(raw_bytes)
    print("Saved:", out)

if __name__ == "__main__":
    main()

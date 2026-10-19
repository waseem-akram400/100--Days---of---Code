
import speedtest
from datetime import datetime


# Apne internet package ki minimum speeds yahan likhein
EXPECTED_DOWNLOAD = 100  # Mbps
EXPECTED_UPLOAD = 20     # Mbps

PROVIDER_NAME = "My Internet Provider"


def check_internet_speed():
    """Internet ki download, upload aur ping speed check karein."""

    print("Internet speed test shuru ho raha hai...")
    print("Thora intezar karein...\n")

    tester = speedtest.Speedtest()
    tester.get_best_server()

    download_speed = tester.download() / 1_000_000
    upload_speed = tester.upload() / 1_000_000
    ping_speed = tester.results.ping

    return download_speed, upload_speed, ping_speed


def create_complaint(download, upload, ping):
    """Speed kam hone par shikayat ka paigham tayar karein."""

    message = (
        f"Hello {PROVIDER_NAME}, my internet speed is below "
        f"my package speed. Download: {download:.2f} Mbps, "
        f"Upload: {upload:.2f} Mbps, Ping: {ping:.2f} ms. "
        "Please check and resolve this issue."
    )

    return message


def main():
    try:
        download, upload, ping = check_internet_speed()

        print("----- Internet Speed Report -----")
        print(f"Date and time: {datetime.now()}")
        print(f"Download speed: {download:.2f} Mbps")
        print(f"Upload speed:   {upload:.2f} Mbps")
        print(f"Ping:           {ping:.2f} ms")

        download_low = download < EXPECTED_DOWNLOAD
        upload_low = upload < EXPECTED_UPLOAD

        if download_low or upload_low:
            print("\nInternet speed package se kam hai.")
            complaint = create_complaint(download, upload, ping)

            print("\nComplaint message:")
            print(complaint)
            print("\nIs message ko check karke aap X par khud post kar sakte hain.")
        else:
            print("\nInternet speed aapki set ki hui target speed ke mutabiq hai.")

    except Exception as error:
        print("\nSpeed test mein masla aaya:")
        print(error)


if __name__ == "__main__":
    main()

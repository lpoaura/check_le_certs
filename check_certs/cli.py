import argparse
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

import pytz
from cryptography import x509
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

DEFAULT_CERTS_DIR = "/certs"


def get_certificate_expiration(cert_path: str) -> datetime:
    """Get the expiration date of a certificate."""
    with open(cert_path, "rb") as cert_file:
        cert_data = cert_file.read()
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
        return cert.not_valid_after_utc


def categorize_certificates(certs_dir: str) -> List[Dict[str, Any]]:
    """Categorize certificates into valid, about to expire, and expired."""
    certificates: List[Dict[str, Any]] = []

    current_date = datetime.now(pytz.utc)  # Use UTC timezone
    threshold_date = current_date + timedelta(days=30)

    try:
        for domain in os.listdir(certs_dir):
            cert_path = os.path.join(certs_dir, domain, "fullchain.pem")
            if os.path.isfile(cert_path):
                expiration_date = get_certificate_expiration(cert_path)
                expiration_str = expiration_date.isoformat()  # Convert to string

                if expiration_date > current_date:
                    status = "valid"
                elif (
                    expiration_date <= current_date and expiration_date > threshold_date
                ):
                    status = "expiring"
                else:
                    status = "expired"

                certificates.append(
                    {
                        "domain": domain,
                        "expiration_date": expiration_str,
                        "status": status,
                    }
                )
    except FileNotFoundError as e:
        logger.error("Certs folder not found")
        exit()

    return certificates


def cli() -> None:
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="List Let's Encrypt certificates.")
    parser.add_argument(
        "--category",
        choices=["all", "valid", "expiring", "expired"],
        default="all",
        help="Specify the category of certificates to list (default: all)",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )
    parser.add_argument(
        "--certs-dir", type=str, help="Directory where certificates are stored"
    )

    args = parser.parse_args()

    certs_dir = os.environ.get("CERTS_DIR", args.certs_dir or DEFAULT_CERTS_DIR)

    # Categorize certificates
    certificates = categorize_certificates(certs_dir)

    # Filter certificates based on the specified category
    if args.category != "all":
        certificates = [
            cert for cert in certificates if cert["status"] == args.category
        ]

    # Print the results
    if args.json:
        print(json.dumps(certificates, indent=4))
    else:
        print("Certificates categorized by status:")
        for cert in certificates:
            print(
                f"Domain: {cert['domain']}, Expiration Date: {cert['expiration_date']}, Status: {cert['status']}"
            )


if __name__ == "__main__":
    cli()

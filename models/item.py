import uuid
from datetime import datetime


class FashionItem:
    def __init__(
        self,
        name,
        item_type,
        platform,
        acquisition_type,
        acquisition_channel,
        price,
        currency_name,
        currency_type,
        catalog_asset_id=None,
        usd_equivalent=None,
        source_experience=None,
        order_id=None,
        notes=None,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.item_type = item_type
        self.platform = platform
        self.acquisition_type = acquisition_type
        self.acquisition_channel = acquisition_channel

        self.price = price
        self.currency_name = currency_name
        self.currency_type = currency_type
        self.usd_equivalent = usd_equivalent

        self.source_experience = source_experience
        self.order_id = order_id
        self.catalog_asset_id = catalog_asset_id
        self.notes = notes

        self.date_acquired = datetime.now().strftime("%Y-%m-%d")

        # 🔥 NEW: audit history
        self.audit_history = []

    # -------------------------
    # Audit Methods
    # -------------------------

    def log_verification(self, status, scanner_version="v1.0"):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": status,  # "present" or "missing"
            "scanner_version": scanner_version,
        }
        self.audit_history.append(entry)

    @property
    def last_verified(self):
        if self.audit_history:
            return self.audit_history[-1]["date"]
        return None

    @property
    def verified_visible(self):
        if self.audit_history:
            return self.audit_history[-1]["status"] == "present"
        return None

    @property
    def missing_flag(self):
        if self.audit_history:
            return self.audit_history[-1]["status"] == "missing"
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "item_type": self.item_type,
            "platform": self.platform,
            "acquisition_type": self.acquisition_type,
            "acquisition_channel": self.acquisition_channel,
            "price": self.price,
            "currency_name": self.currency_name,
            "currency_type": self.currency_type,
            "usd_equivalent": self.usd_equivalent,
            "source_experience": self.source_experience,
            "order_id": self.order_id,
            "catalog_asset_id": self.catalog_asset_id,
            "notes": self.notes,
            "date_acquired": self.date_acquired,
            "last_verified": self.last_verified,
            "verified_visible": self.verified_visible,
            "missing_flag": self.missing_flag,
            "audit_history": self.audit_history,
        }
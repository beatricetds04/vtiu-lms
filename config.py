import os


class Config:
        # ------------------------------------------------------
        # CORE
        # ------------------------------------------------------
        # Require a real secret in production so CSRF/session tokens remain valid
        # across deploys and app restarts. Local development may still fall back to
        # a generated ephemeral secret to avoid blocking startup in non-prod.
        def _production_environment():
            return bool(
                os.environ.get("IS_PRODUCTION") in ("1", "true", "True")
                or os.environ.get("FLASK_ENV", "").lower() == "production"
                or os.environ.get("RAILWAY_ENVIRONMENT")
                or os.environ.get("RAILWAY_ENVIRONMENT_NAME")
                or os.environ.get("RAILWAY_PROJECT_ID")
                or os.environ.get("RAILWAY_SERVICE_ID")
            )

        SECRET_KEY = os.environ.get("SECRET_KEY")
        if not SECRET_KEY:
            if _production_environment():
                raise RuntimeError(
                    "SECRET_KEY is required in production. Set it in Railway/your environment "
                    "before starting the app."
                )
            SECRET_KEY = "dev-secret-key"

        # Paystack credentials are supplied through deployment environment variables.
        PAYSTACK_TEST_SECRET_KEY = os.environ.get("PAYSTACK_TEST_SECRET_KEY", "")
        PAYSTACK_TEST_PUBLIC_KEY = os.environ.get("PAYSTACK_TEST_PUBLIC_KEY", "")
        PAYSTACK_LIVE_SECRET_KEY = os.environ.get("PAYSTACK_LIVE_SECRET_KEY", "")
        PAYSTACK_LIVE_PUBLIC_KEY = os.environ.get("PAYSTACK_LIVE_PUBLIC_KEY", "")
        PAYSTACK_CURRENCY = os.environ.get("PAYSTACK_CURRENCY", "GHS")
        PAYSTACK_TEST_CALLBACK_URL = os.environ.get(
            "PAYSTACK_TEST_CALLBACK_URL",
            "https://vtiu-lms-production.up.railway.app/student/paystack/callback"
        )
        PAYSTACK_LIVE_CALLBACK_URL = os.environ.get(
            "PAYSTACK_LIVE_CALLBACK_URL",
            "https://vtiu-lms-production.up.railway.app/student/paystack/callback"
        )
        PAYSTACK_CALLBACK_URL = os.environ.get(
            "PAYSTACK_CALLBACK_URL",
            "https://vtiu-lms-production.up.railway.app/student/paystack/callback"
        )
        PAYSTACK_TEST_WEBHOOK_URL = os.environ.get(
            "PAYSTACK_TEST_WEBHOOK_URL",
            "https://vtiu-lms-production.up.railway.app/api/paystack/webhook"
        )
        PAYSTACK_LIVE_WEBHOOK_URL = os.environ.get(
            "PAYSTACK_LIVE_WEBHOOK_URL",
            "https://vtiu-lms-production.up.railway.app/api/paystack/webhook"
        )

        # DATABASE (Railway PostgreSQL)
        db_url = os.environ.get("DATABASE_URL")

        if not db_url:
            raise RuntimeError(
                "DATABASE_URL is required. Configure the Railway PostgreSQL "
                "connection before starting the application."
            )

        SQLALCHEMY_DATABASE_URI = db_url.replace("postgres://", "postgresql://", 1)

        # Railway PostgreSQL requires SSL for external connections.
        if "sslmode=" not in SQLALCHEMY_DATABASE_URI:
            separator = "&" if "?" in SQLALCHEMY_DATABASE_URI else "?"
            SQLALCHEMY_DATABASE_URI += f"{separator}sslmode=require"

        SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        # Aggressive connection pool settings for production (prevent memory issues)
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": 3,         # Further reduced from 5
            "pool_recycle": 120,    # Further reduced from 180 (2 minutes)
            "pool_pre_ping": True,
            "max_overflow": 5,       # Further reduced from 10
            "pool_timeout": 30,     # Add timeout for getting connections
            "pool_reset_on_return": "commit"  # Reset connections on return
        }

        MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB uploads

        # Aggressive memory management settings
        MEMORY_LIMIT_MB = 256  # Reduced from 512 - more aggressive threshold
        
        # More frequent cleanup settings
        CLEANUP_INTERVAL = 180  # Reduced from 300 (3 minutes)

        # ------------------------------------------------------
        # BASE DIRECTORY
        # ------------------------------------------------------
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))

        # ------------------------------------------------------
        # ADMISSIONS
        # ------------------------------------------------------
        VOUCHER_DEFAULT_AMOUNT = 220.0

        # ------------------------------------------------------
        # FILE UPLOADS
        # ------------------------------------------------------
        UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "assignments")
        MATERIALS_FOLDER = os.path.join(BASE_DIR, "uploads", "materials")

        PAYMENT_PROOF_FOLDER = os.path.join(
            BASE_DIR, "static", "uploads", "payments"
        )
        RECEIPT_FOLDER = os.path.join(
            BASE_DIR, "static", "uploads", "receipts"
        )
        PROFILE_PICS_FOLDER = os.path.join(
            BASE_DIR, "static", "uploads", "profile_pictures"
        )

        # ------------------------------------------------------
        # EMAIL CONFIGURATION (BREVO HTTPS API)
        # ------------------------------------------------------
        BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
        BREVO_DEFAULT_SENDER = os.environ.get("BREVO_DEFAULT_SENDER", "lampteyjoseph860@gmail.com")
        
        # Use verified Gmail sender for immediate delivery
        MAIL_DEFAULT_SENDER = os.environ.get("BREVO_DEFAULT_SENDER", "lampteyjoseph860@gmail.com")

        # ------------------------------------------------------
        # AGORA RTC
        # ------------------------------------------------------
        AGORA_APP_ID = os.environ.get("AGORA_APP_ID", "").strip()
        AGORA_APP_CERTIFICATE = os.environ.get("AGORA_APP_CERTIFICATE", "").strip()
        AGORA_CHANNEL_PROFILE = os.environ.get("AGORA_CHANNEL_PROFILE", "live").strip().lower()
        REDIS_URL = os.environ.get("REDIS_URL", "").strip()

        # Legacy Zoom configuration is intentionally inactive. Keep these values
        # available for a future rollback without using them in the active flow.
        # ZOOM_ACCOUNT_ID = os.environ.get("ZOOM_ACCOUNT_ID")
        # ZOOM_CLIENT_ID = os.environ.get("ZOOM_CLIENT_ID")
        # ZOOM_CLIENT_SECRET = os.environ.get("ZOOM_CLIENT_SECRET")

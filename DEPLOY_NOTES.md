# RevenueCat Apple IAP Deploy Notes

## Completed from this session

- ClipForge AI production URL: `https://www.clipforge.ai`
- Vercel root directory: `frontend`
- Production env var added in Vercel:
  - `REVENUECAT_WEBHOOK_AUTH_HEADER`
  - Source: copy the value from local `frontend/.env`
- Optional override vars were not present in local `frontend/.env`, so they were not set:
  - `REVENUECAT_PRO_PRODUCT_IDS`
  - `REVENUECAT_SCALE_PRODUCT_IDS`

## Manual production steps still required

1. Confirm `REVENUECAT_WEBHOOK_AUTH_HEADER` exists in the production environment for ClipForge AI.

2. If custom RevenueCat product identifiers are needed, set these Vercel Production env vars from the production billing configuration:
   - `REVENUECAT_PRO_PRODUCT_IDS`
   - `REVENUECAT_SCALE_PRODUCT_IDS`

3. Run the Prisma migration against the production frontend database only after positively identifying the production `DATABASE_URL`:

   ```bash
   cd frontend
   DATABASE_URL="<production-database-url>" npx prisma migrate deploy
   ```

4. Apply the backend SQL migration against the production backend database:

   ```bash
   psql "<production-backend-database-url>" -f backend/migrations/003_add_revenuecat_subscription_provider.sql
   ```

5. Deploy/redeploy production after the database migrations have completed.

6. Verify the RevenueCat dashboard webhook URL is configured as:

   ```text
   https://www.clipforge.ai/api/billing/revenuecat-webhook
   ```

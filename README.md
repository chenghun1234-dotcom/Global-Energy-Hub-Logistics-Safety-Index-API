# Global Energy Hub & Logistics Safety-Index API

A deterministic API for global energy logistics, maritime route safety, and energy tax calculations. Built for zero operating costs using serverless architecture and automated data syncing.

## 🚀 Key Features
- **Route Safety Scores**: Deterministic risk calculation for major maritime chokepoints.
- **Energy Tax Logic**: Precise calculation of tariffs, VAT, and storage fees across global hubs.
- **Infrastructure Specs**: Data on terminal capacities, draughts, and vessel compatibility.
- **Automated Benchmarks**: Daily data sync from **EIA** and **Opinet** via GitHub Actions.

## 🛠️ Technology Stack
- **Backend**: FastAPI (Python)
- **Deployment**: Vercel / Cloudflare Workers
- **Automation**: GitHub Actions
- **Data**: Static JSON (Deterministic Engine)

## 📦 Setup & Deployment
1. **Repository Secrets**: Add the following to your GitHub Actions secrets:
   - `EIA_API_KEY`: Your EIA Open Data key.
   - `OPINET_API_KEY`: Your Opinet API code.
2. **Installation**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Local Dev**:
   ```bash
   uvicorn main:app --reload
   ```

## 📄 Documentation
The landing page with full API documentation is built-in and can be accessed at the root path `/` when deployed.

---
*Built with ❤️ for Global Energy Logistics.*

# bindays

Source code for the website [bindays](https://bindays.uk) which shows the bin days for Edinburgh, Scotland.

The website runs in 3 docker containers:

1. React app frontend with nginx server
2. Python backend, running a flask API
3. Mongo DB

All data is scraped from the Edinburgh City Council bin schedule PDFs.

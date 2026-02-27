# Skill Management (Flask)

This project is a Flask-based skill management app with:

- Admin login and dashboard
- Student dashboard
- Neon Postgres-backed storage for users, students, and skills

## Local run

1. Create a Neon project and copy its Postgres connection string.

2. Export environment variables:

	```bash
	export DATABASE_URL="postgresql://..."
	export SECRET_KEY="change-me"
	```

3. Install dependencies:

	 ```bash
	 pip install -r requirements.txt
	 ```

4. Start the app:

	 ```bash
	 python app.py
	 ```

5. Open:

	 ```
	 http://127.0.0.1:5000
	 ```

## Vercel deployment

This repository is now configured for Vercel with `vercel.json` using `@vercel/python`.

### Deploy with Vercel CLI

1. Install CLI (if needed):

	```bash
	npm i -g vercel
	```

2. Login and deploy from the project root:

	```bash
	vercel
	```

3. For production deploy:

	```bash
	vercel --prod
	```

4. In your Vercel project settings, add environment variables:

	- `DATABASE_URL` = Neon connection string
	- `SECRET_KEY` = secure random string

## Environment variables

- `SECRET_KEY`: Flask session secret
- `DATABASE_URL`: required Postgres connection string (Neon)
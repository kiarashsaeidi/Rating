# Rating
This project implements an optimized rating system using Django, Redis, and Celery to efficiently handle large volumes of user ratings without overloading the database. Instead of storing ratings instantly, new ratings are temporarily cached in Redis and periodically processed in batches to update the database.

CREATE TABLE "clean_data_df" (
    "incident_name" VARCHAR   NOT NULL,
    "county" VARCHAR   NOT NULL,
    "acres_burned" FLOAT DEFAULT NULL,
    "longitude" FLOAT DEFAULT NULL,
    "latitude" FLOAT DEFAULT NULL,
    "incident_type" VARCHAR   NOT NULL,
    "date_extinguished" FLOAT DEFAULT NULL,
    "date_created" FLOAT DEFAULT NULL
);
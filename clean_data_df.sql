CREATE TABLE "clean_data_df" (
    "incident_name" VARCHAR   NOT NULL,
    "county" VARCHAR   NOT NULL,
    "acres_burned" int   NOT NULL,
    "longitude" int   NOT NULL,
    "latitude" int   NOT NULL,
    "incident_type" VARCHAR   NOT NULL,
    "date_extinguished" date   NOT NULL,
    "date_created" date   NOT NULL
);
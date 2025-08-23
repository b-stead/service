-- Main user table
CREATE TABLE "user" (
    "user_id" text NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::text,
    "sub" text NOT NULL, -- Identifier from Firebase,
    "email" text NOT NULL,
    "email_verified" boolean NULL DEFAULT false,
    "first_name" text NOT NULL,
    "last_name" text NOT NULL,
    "birthdate" date NULL,
    "created_date" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "is_deleted" boolean NOT NULL DEFAULT false,
    "deleted_at" timestamp NULL
);
-- These indexes express that sub/email must be unique for active (i.e. not deleted) users
CREATE UNIQUE INDEX ON "user" ("sub") WHERE "is_deleted" = FALSE;
CREATE UNIQUE INDEX ON "user" ("email") WHERE "is_deleted" = FALSE;
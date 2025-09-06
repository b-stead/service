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

-- Customers Table
CREATE TABLE "customers" (
    "customer_id" text NOT NULL PRIMARY KEY DEFAULT gen_random_uuid()::text,
    "user_id" text NOT NULL REFERENCES "user"("user_id"),
    "name" text,
    "company_name" text,
    "organisation" boolean DEFAULT false,
    "contact_person" text,
    "email" text,
    "phone" text,
    "address_line1" text,
    "address_line2" text,
    "city" text,
    "state" text,
    "postal_code" text,
    "country" text,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" boolean NOT NULL DEFAULT false,
    "deleted_at" timestamp NULL
);

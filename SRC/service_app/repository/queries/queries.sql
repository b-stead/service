-- name: CreateUser :one
INSERT INTO "user" (
    "sub",
    "email",
    "first_name",
    "last_name",
    "birthdate"
)
VALUES (
    $1,
    $2,
    $3,
    $4,
    $5
) RETURNING *;

-- name: GetUserBySub :one
SELECT * FROM "user" WHERE "sub" = $1;


-- name: CreateCustomer :one
INSERT INTO "customers" (
    "user_id",
    "company_name",
    "contact_person",
    "email",
    "phone",
    "address_line1",
    "address_line2",
    "city",
    "state",
    "postal_code",
    "country"
) VALUES (
    (SELECT "user_id" FROM "user" WHERE "sub" = $1 AND "is_deleted" = FALSE),
    $2, $3, $4, $5, $6, $7, $8, $9, $10, $11
) RETURNING *;
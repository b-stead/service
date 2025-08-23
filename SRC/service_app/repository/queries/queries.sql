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

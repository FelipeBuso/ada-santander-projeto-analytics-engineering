-- CreateTable
CREATE TABLE "listining" (
    "id" SERIAL NOT NULL,
    "listining_id" INTEGER NOT NULL,
    "listing_url" VARCHAR NOT NULL,
    "scrape_id" BIGINT NOT NULL,
    "host_id" INTEGER NOT NULL,
    "host_listings_count" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "listining_pkey" PRIMARY KEY ("id")
);

/*
  Warnings:

  - A unique constraint covering the columns `[listining_id]` on the table `listining` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateTable
CREATE TABLE "reviews" (
    "id" SERIAL NOT NULL,
    "listing_id" INTEGER NOT NULL,
    "review_id" INTEGER NOT NULL,
    "date" TEXT NOT NULL,
    "reviewer_id" INTEGER NOT NULL,
    "reviewer_name" TEXT NOT NULL,
    "comments" TEXT,
    "listiningId" INTEGER,

    CONSTRAINT "reviews_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "listining_listining_id_key" ON "listining"("listining_id");

-- AddForeignKey
ALTER TABLE "reviews" ADD CONSTRAINT "reviews_listing_id_fkey" FOREIGN KEY ("listing_id") REFERENCES "listining"("listining_id") ON DELETE RESTRICT ON UPDATE CASCADE;

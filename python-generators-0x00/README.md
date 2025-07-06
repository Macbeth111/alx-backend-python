Python Generators and MySQL ETL Task
📚 Overview

This project explores the use of Python generators to efficiently interact with a MySQL database. It focuses on creating scalable, memory-efficient data pipelines that stream, batch, paginate, and process large volumes of user data without overloading system memory.

The project is structured as a sequence of four tasks, each building on the previous to simulate real-world backend data operations.
🧩 Project Structure

Repository: alx-backend-python
Directory: python-generators-0x00
Main Files:

    seed.py – database setup and CSV data loader
    0-stream_users.py – row-by-row generator
    1-batch_processing.py – batch generator and processor
    2-lazy_paginate.py – lazy paginator
    4-stream_ages.py – memory-efficient aggregation

0. 📦 Database Setup with seed.py

Objective:
Set up a MySQL database (ALX_prodev) and load user data from user_data.csv.

Features:

    Creates user_data table with:
        user_id (UUID, Primary Key)
        name, email, age
    Inserts data with INSERT IGNORE to handle duplicates
    Prototypes:

    def connect_db()
    def create_database(connection)
    def connect_to_prodev()
    def create_table(connection)
    def insert_data(connection, data)


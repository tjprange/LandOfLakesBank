-- This file will represent the queries needed for each page on the frontend of
-- our website. Any variable that we expect the backend code to pass to these 
-- queries will be denoted by surrounding curly braces: {} 


-- Add Client Page
-- This Form will add a Client and their Address to the database. A client must 
-- have an address, and so the form is consolodated here.

INSERT INTO `addresses` (`city`, `state`, `house_number`, `zip_code`)
VALUES ('{city}', '{state}', '{house_number}', '{zip_code}');

INSERT INTO `clients`(`ssn`, `first_name`, `last_name`, `email`, `address_id`)
VALUES ({ssn}, '{first_name}', '{last_name}', '{email}', '{address_id}');



-- Add Financial Advisor Page
-- This form will an advisor to the database. By default, advisors do not have 
-- a book of clients

INSERT INTO `financial_advisors` (`area_of_expertise`, `first_name`, `last_name`)
VALUES ('{area_of_expertise}', '{first_name}', '{last_name}');


-- Add an Account Page
-- This form will add an account for the requested client(s).

-- First we create the account

INSERT INTO `accounts` (`balance`)
VALUES ({balance});

-- Second, we link the account with the client(s) that the user asked to make an
-- account for (accounts MUST have users. Only joint accounts allowed for multi-
-- users)

INSERT INTO `clients_accounts` (`client_id`, `account_id`)
VALUES ('{client_id}', '{account_id}');
-- (Do again for joint accounts)


-- Update Client Page
-- This form will update all fields for the client passed in with their ID
-- It will also update their address, if wanted.

UPDATE `clients`
SET
        `ssn` = {ssn},
        `first_name` = {first_name},
        `last_name` = {last_name},
        `email` = {email}
WHERE
        `client_id` = {client_id};

-- Because the addresses relationship to clients are nullable, we have three scenarios:
-- 1) That we need to update the current address

UPDATE `addresses`
SET
        `city` = {city},
        `state` = {state},
        `house_number` = {house_number},
        `zip_code` = {zip_code}
WHERE
        `address_id` = {address_id};

-- 2) That we need to create a new address
INSERT INTO `addresses` (`city`, `state`, `house_number`, `zip_code`)
VALUES ('{city}', '{state}', '{house_number}', '{zip_code}');

-- 3) That we need to nullify (delete) an address
DELETE FROM `addresses`
WHERE `address_id` = {address_id}

-- Connect Advisor Page
-- This form will connect an advisor with a client using their respective IDs

INSERT INTO `clients_advisors` (`client_id`, `advisor_id`)
VALUES ('{client_id}', '{advisor_id}');

-- Delete Account Page 

-- This will look up the accounts associated with the id.
SELECT * FROM `accounts` WHERE `account_id` = {account_id};
-- and delete the account from the user with the specified account id
DELETE FROM `accounts` WHERE `account_id` = {account_id};

-- Search The Database
-- TO DO: We will search a client by id and populate requested data

SELECT * FROM `clients` WHERE last_name LIKE '{search_term}%'

-- View Tables

-- Clients

SELECT
        `client_id` as 'Client ID',
        `ssn` as 'Social Security Number',
        CONCAT(`first_name`, ' ', `last_name`) as 'Client Name',
        `email` as 'Email'
FROM
        `clients`;

-- Accounts

SELECT
        `account_id` as 'Account Number',
        `balance` as 'Account Balance'
FROM
        `accounts`;

-- Clients Accounts

SELECT `client_account_id` as 'Client Account ID',
       clients.first_name as 'First Name',
       clients.last_name as 'Last Name',
       clients.client_id as 'Client ID',
       accounts.account_id as 'Account ID'
FROM `clients_accounts`
INNER JOIN clients ON clients.client_id=clients_accounts.client_id
INNER JOIN accounts ON accounts.account_id=clients_accounts.account_id;        

-- Addresses

SELECT
        `address_id` as 'Address ID',
        `city` as 'City',
        `state` as 'State',
        `house_number` as 'House Number',
        `zip_code` as 'Zip Code'
FROM
        `addresses`;

-- Financial Advisors

SELECT
        `advisor_id` as 'Advisor ID',
        CONCAT(`first_name`, ' ', `last_name`) as 'Advisor Name',
        `area_of_expertise` as 'Area of Expertise'
FROM
        `financial_advisors`;

-- Clients Advisors

SELECT `client_advisor_id` as 'Client Advisor ID',
        clients.client_id as 'Client ID',
        clients.first_name as 'C First',
        clients.last_name as 'C Last',
        financial_advisors.advisor_id as 'Advisor ID',
        financial_advisors.first_name as 'A First',
        financial_advisors.last_name as 'A Last'
FROM `clients_advisors`
INNER JOIN clients ON clients.client_id=clients_advisors.client_id
INNER JOIN financial_advisors ON financial_advisors.advisor_id=clients_advisors.advisor_id;

-- drop table desc_report;
-- INSERT INTO desc_report ( Market, Store, Store_ID, Store_Limit, Override_Disc, Disc_SKU, EOL, Aging, Cx_Survey, MD_approved, Comment) VALUES ('MUSHAF', 'Store1', '123', 1800, 10.5, 5.0, 1, 3.0, 4.5, 1.0, 'TEST' );
-- SHOW TRIGGERS;
-- DROP TRIGGER IF EXISTS insert_desc_report_values;
-- UPDATE desc_report SET Store_Limit = 180 WHERE Store_ID = '126533';
-- DELETE FROM desc_report;
-- TRUNCATE TABLE desc_report;

--------------------------------------------------------------------------------------------------------------
CREATE TABLE desc_report (
    Market VARCHAR(255),
    Store VARCHAR(255),
    Store_ID VARCHAR(255) PRIMARY KEY,
    Store_Limit INT,
    Override_Disc FLOAT null,
    Disc_SKU FLOAT null,
    Total_Availed FLOAT null,
    Remaining FLOAT null,
    EOL FLOAT null,
    Aging FLOAT null,
    Cx_Survey FLOAT null,
    MD_approved FLOAT null,
    Comment VARCHAR(255)
);
--------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------
DELIMITER $$
CREATE TRIGGER insert_desc_report_values
BEFORE INSERT ON desc_report
FOR EACH ROW
BEGIN
    DECLARE new_Total_Availed FLOAT;
    DECLARE new_Remaining FLOAT;

    -- Calculate Total_Availed
    SET new_Total_Availed = (IFNULL(NEW.Override_Disc, 0) + IFNULL(NEW.Disc_SKU, 0)) - 
                            (IFNULL(NEW.EOL, 0) + IFNULL(NEW.Aging, 0) + IFNULL(NEW.Cx_Survey, 0));
                            
    -- Calculate Remaining
    SET new_Remaining = (NEW.Store_Limit + IFNULL(NEW.MD_approved, 0)) - new_Total_Availed;

    -- Assign the calculated values to the NEW row
    SET NEW.Total_Availed = new_Total_Availed;
    SET NEW.Remaining = new_Remaining;
END$$
DELIMITER ;
--------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------
DELIMITER $$
CREATE TRIGGER update_desc_report_values
BEFORE UPDATE ON desc_report
FOR EACH ROW
BEGIN
    DECLARE new_Total_Availed FLOAT;
    DECLARE new_Remaining FLOAT;

    -- Calculate Total_Availed
    SET new_Total_Availed = (IFNULL(NEW.Override_Disc, 0) + IFNULL(NEW.Disc_SKU, 0)) - 
                            (IFNULL(NEW.EOL, 0) + IFNULL(NEW.Aging, 0) + IFNULL(NEW.Cx_Survey, 0));

    -- Calculate Remaining
    SET new_Remaining = (NEW.Store_Limit + IFNULL(NEW.MD_approved, 0)) - new_Total_Availed;

    -- Assign the calculated values to the NEW row
    SET NEW.Total_Availed = new_Total_Availed;
    SET NEW.Remaining = new_Remaining;
END$$
DELIMITER ;
--------------------------------------------------------------------------------------------------------------

UPDATE desc_report 
SET 
    EOL = 50,
    Aging = 50,
    Cx_Survey = 50,
    MD_approved = 50
WHERE Store_ID = 'XTHAL1149';

select * from desc_report ;

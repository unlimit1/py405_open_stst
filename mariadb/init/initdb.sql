-- 증권정보 수집용 DB 및 USER 생성
CREATE DATABASE finance;
CREATE USER 'u_fina'@'%' IDENTIFIED BY 'dbfinapw';
GRANT ALL PRIVILEGES ON finance.* TO 'u_fina'@'%';
FLUSH PRIVILEGES;

-- airflow 용 DB 및 USER 생성
CREATE DATABASE airflow;
CREATE USER `u_airflow`@`%` IDENTIFIED BY 'dbairfpw';
GRANT ALL PRIVILEGES ON airflow.* TO `u_airflow`@`%`;
FLUSH PRIVILEGES;

CREATE TABLE finance.naver_daily_ohlcv (
    stock_code VARCHAR(20) NOT NULL COMMENT '종목코드',
    stock_name VARCHAR(200) NOT NULL COMMENT '종목명명',
    trade_date DATE NOT NULL COMMENT '거래일자',
    open_price FLOAT NOT NULL COMMENT '시가',
    high_price FLOAT NOT NULL COMMENT '고가',
    low_price FLOAT NOT NULL COMMENT '저가',
    close_price FLOAT NOT NULL COMMENT '종가',
    volume INT NOT NULL COMMENT '거래량',
    -- foreigner_ratio FLOAT NOT NULL COMMENT '외국인소진율',
    insert_datetime DATETIME NOT NULL COMMENT '저장일시',
	PRIMARY KEY (`stock_code`, `trade_date` desc) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

CREATE TABLE finance.heartbeat_by_airflow (
    app_datetime DATETIME(6),
    db_datetime DATETIME(6),
    INDEX idx_app_datetime (app_datetime desc)
);

CREATE TABLE finance.naver_financial_indicator_value (
  crawling_datetime datetime NOT NULL, 
  stock_code VARCHAR(20) NOT NULL,
  financial_indicator_name varchar(100) NOT NULL,
  quarter_ym varchar(10) NOT NULL,
  year_quarter_cl varchar(10) NOT NULL,
  accounting_standard_name varchar(20) NOT NULL,
  prediction_yn varchar(10) NOT NULL,
  financial_indicator_value double,
  crawling_origin_text VARCHAR(200),
  PRIMARY KEY (crawling_datetime,stock_code,financial_indicator_name,quarter_ym,year_quarter_cl,accounting_standard_name,prediction_yn)
  ,INDEX idx01 (stock_code,financial_indicator_name,quarter_ym,year_quarter_cl,accounting_standard_name,prediction_yn)
) ENGINE=InnoDB DEFAULT CHARSET=utf8; 
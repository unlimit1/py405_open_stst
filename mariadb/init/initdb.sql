CREATE DATABASE finance;
CREATE USER 'u_fina'@'%' IDENTIFIED BY 'fina!@34';
GRANT ALL PRIVILEGES ON finance.* TO 'u_fina'@'%';
FLUSH PRIVILEGES;

CREATE TABLE finance.naver_daily_ohlcv (
    stock_code VARCHAR(20) NOT NULL COMMENT '종목코드',
    trade_date DATE NOT NULL COMMENT '거래일자',
    open_price FLOAT NOT NULL COMMENT '시가',
    high_price FLOAT NOT NULL COMMENT '고가',
    low_price FLOAT NOT NULL COMMENT '저가',
    close_price FLOAT NOT NULL COMMENT '종가',
    volume INT NOT NULL COMMENT '거래량',
    foreigner_ratio FLOAT NOT NULL COMMENT '외국인소진율',
    insert_datetime DATETIME NOT NULL COMMENT '저장일시',
	PRIMARY KEY (`stock_code`, `trade_date`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
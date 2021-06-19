DROP TABLE IF EXISTS payroll_item;
DROP TABLE IF EXISTS payroll;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS role;

CREATE TABLE role(
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128)
);

CREATE TABLE employee
(
    id               INTEGER AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(255) NOT NULL,
    cpf              VARCHAR(16)  NOT NULL,
    rg               VARCHAR(16)  NOT NULL,
    birth_date       DATE         NOT NULL,
    role_id          INTEGER NOT NULL,
    hire_date        DATE         NOT NULL,
    resignation_date DATE,
    salary  DECIMAL(10,2),

    CONSTRAINT fk_employee_role FOREIGN KEY (role_id)
        REFERENCES role (id)
);

CREATE TABLE payroll
(
    id           INTEGER AUTO_INCREMENT PRIMARY KEY,
    employee_id  INTEGER NOT NULL,
    amount       DECIMAL NOT NULL,
    paid         BOOLEAN,
    payment_date DATE    NOT NULL,

    CONSTRAINT fk_payroll_employee FOREIGN KEY (employee_id)
        REFERENCES employee (id)
);

CREATE TABLE payroll_item
(
    id          INTEGER AUTO_INCREMENT PRIMARY KEY,
    payroll_id  INTEGER NOT NULL,
    description VARCHAR(255),
    type        VARCHAR(64),
    amount      DECIMAL NOT NULL,

    CONSTRAINT fk_payroll_items_payroll FOREIGN KEY (payroll_id)
        REFERENCES payroll (id)
);


INSERT INTO role VALUES(DEFAULT, 'Administração');
INSERT INTO role VALUES(DEFAULT, 'Técnico');
INSERT INTO role VALUES(DEFAULT, 'Atendimento');
INSERT INTO role VALUES(DEFAULT, 'Financeiro');
INSERT INTO role VALUES(DEFAULT, 'RH');

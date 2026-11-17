-- Proactive Ticketing Queue: SQL Server schema
-- Column order of Tickets matters: app.py reads SELECT * as id, title, description, category, status.

IF DB_ID('ProactiveTQ') IS NULL CREATE DATABASE ProactiveTQ;
GO
USE ProactiveTQ;
GO

CREATE TABLE Tickets (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    title       NVARCHAR(200)  NOT NULL,
    description NVARCHAR(MAX)  NULL,
    category    NVARCHAR(100)  NULL,
    status      NVARCHAR(20)   NOT NULL DEFAULT 'Open'
        CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    created_at  DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE TABLE WorkLogs (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    ticket_id   INT            NOT NULL REFERENCES Tickets(id) ON DELETE CASCADE,
    message     NVARCHAR(MAX)  NOT NULL,
    created_at  DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

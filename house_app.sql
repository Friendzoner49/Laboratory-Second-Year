-- Tạo bảng `orders`
CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_res TEXT NOT NULL,
  name_ser TEXT NOT NULL,
  amount INTEGER NOT NULL,
  total_cost REAL NOT NULL
);

-- Tạo bảng `residents`
CREATE TABLE residents (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  last_name TEXT NOT NULL,
  first_name TEXT NOT NULL,
  bonus REAL DEFAULT 0
);

-- Thêm dữ liệu vào bảng `residents`
INSERT INTO residents (ID, last_name, first_name, bonus) VALUES
(1, 'vu', 'hung', 0.3),
(2, 'vu', 'huy', 0.5);

-- Tạo bảng `services`
CREATE TABLE services (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  price NUMERIC
);

-- Tạo bảng `totalcost_sys`
CREATE TABLE totalcost_sys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,  -- Thêm ràng buộc UNIQUE
    total_cost REAL NOT NULL
);

-- Tạo bảng `user_list`
CREATE TABLE user_list (
  user TEXT,
  pass TEXT
);

-- Thêm dữ liệu vào bảng `user_list`
INSERT INTO user_list (user, pass) VALUES
('admin', '123'),
('admin', '456'),
('hi', '');

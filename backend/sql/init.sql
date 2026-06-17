CREATE DATABASE IF NOT EXISTS music_school_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE music_school_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    real_name VARCHAR(50),
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'teacher',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    instrument VARCHAR(50),
    level VARCHAR(20) DEFAULT 'intermediate',
    bio TEXT,
    hire_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    parent_name VARCHAR(50),
    parent_phone VARCHAR(20),
    birthday DATE,
    level VARCHAR(20) DEFAULT 'beginner',
    remark TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instrument VARCHAR(50),
    duration_minutes INT DEFAULT 45,
    price DECIMAL(10,2) DEFAULT 0,
    max_students INT DEFAULT 1,
    teacher_id INT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS classrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    capacity INT DEFAULT 4,
    piano_count INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'available',
    remark VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS course_schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    classroom_id INT,
    teacher_id INT,
    weekday INT NOT NULL,
    start_time VARCHAR(10) NOT NULL,
    end_time VARCHAR(10) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    schedule_id INT,
    total_lessons INT DEFAULT 12,
    used_lessons INT DEFAULT 0,
    amount DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (schedule_id) REFERENCES course_schedules(id)
);

CREATE TABLE IF NOT EXISTS lesson_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT,
    lesson_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'attended',
    content TEXT,
    homework TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
);

CREATE TABLE IF NOT EXISTS exam_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    exam_name VARCHAR(100) NOT NULL,
    instrument VARCHAR(50),
    level VARCHAR(50),
    exam_date DATE,
    result VARCHAR(20),
    score VARCHAR(20),
    certificate_no VARCHAR(100),
    remark TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS instruments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50),
    model VARCHAR(50),
    serial_no VARCHAR(100),
    status VARCHAR(20) DEFAULT 'available',
    purchase_date DATE,
    price DECIMAL(10,2) DEFAULT 0,
    remark TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Seed data
INSERT INTO users (username, password_hash, real_name, phone, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/I1K', '管理员', '13800138000', 'admin'),
('teacher1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/I1K', '王老师', '13800138001', 'teacher'),
('manager1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/I1K', '李经理', '13800138002', 'manager');

INSERT INTO teachers (name, phone, instrument, level, bio, hire_date) VALUES
('王老师', '13811112222', '钢琴', 'senior', '十年钢琴教学经验', '2019-03-01'),
('陈老师', '13822223333', '小提琴', 'senior', '音乐学院毕业', '2020-06-15'),
('张老师', '13833334444', '吉他', 'intermediate', '民谣吉他教学', '2021-09-10'),
('刘老师', '13844445555', '古筝', 'senior', '古筝演奏级', '2018-01-20');

INSERT INTO students (name, phone, parent_name, parent_phone, birthday, level) VALUES
('小明', '13900001111', '李先生', '13900001112', '2015-04-10', 'beginner'),
('小红', '13900002222', '王女士', '13900002223', '2014-07-22', 'intermediate'),
('小华', '13900003333', '张先生', '13900003334', '2016-01-05', 'beginner'),
('小丽', '13900004444', '赵女士', '13900004445', '2013-11-18', 'advanced');

INSERT INTO courses (name, instrument, duration_minutes, price, max_students, teacher_id, description) VALUES
('少儿钢琴启蒙班', '钢琴', 45, 200.00, 1, 1, '适合零基础儿童'),
('小提琴进阶班', '小提琴', 60, 260.00, 2, 2, '二级以上水平'),
('民谣吉他速成班', '吉他', 45, 150.00, 3, 3, '成人零基础速成'),
('古筝考级班', '古筝', 60, 220.00, 2, 4, '备战三级考级');

INSERT INTO classrooms (name, capacity, piano_count, status, remark) VALUES
('钢琴房A', 2, 1, 'available', '三角钢琴'),
('钢琴房B', 2, 1, 'available', '立式钢琴'),
('小提琴室', 4, 0, 'available', '隔音房'),
('综合教室', 6, 1, 'available', '多功能教室');

INSERT INTO course_schedules (course_id, classroom_id, teacher_id, weekday, start_time, end_time, start_date, end_date) VALUES
(1, 1, 1, 5, '16:00', '16:45', '2026-06-01', '2026-12-31'),
(1, 2, 1, 6, '10:00', '10:45', '2026-06-01', '2026-12-31'),
(2, 3, 2, 5, '18:00', '19:00', '2026-06-01', '2026-12-31'),
(3, 4, 3, 6, '14:00', '14:45', '2026-06-01', '2026-12-31'),
(4, 4, 4, 0, '09:00', '10:00', '2026-06-01', '2026-12-31');

INSERT INTO enrollments (student_id, course_id, schedule_id, total_lessons, used_lessons, amount, status) VALUES
(1, 1, 1, 24, 8, 4800.00, 'active'),
(2, 2, 3, 12, 3, 3120.00, 'active'),
(3, 3, 4, 12, 1, 1800.00, 'active'),
(4, 4, 5, 16, 5, 3520.00, 'active');

INSERT INTO lesson_records (enrollment_id, lesson_date, status, content, homework) VALUES
(1, '2026-06-09', 'attended', '复习C大调音阶，学习二分音符', '每天练琴20分钟'),
(2, '2026-06-09', 'attended', '练习空弦，学习D大调', '练习空弦10分钟'),
(3, '2026-06-08', 'absent', NULL, NULL),
(4, '2026-06-08', 'attended', '古筝摇指技法', '复习《渔舟唱晚》前半段');

INSERT INTO exam_records (student_id, exam_name, instrument, level, exam_date, result, score, certificate_no, remark) VALUES
(2, '2026年夏季小提琴考级', '小提琴', '三级', '2026-07-15', 'pending', NULL, NULL, '备考中'),
(4, '2026年古筝考级', '古筝', '四级', '2026-08-10', 'pending', NULL, NULL, '备考中');

INSERT INTO instruments (name, brand, model, serial_no, status, purchase_date, price, remark) VALUES
('三角钢琴', 'Yamaha', 'GB1K', 'YP2024001', 'available', '2024-01-10', 68000.00, NULL),
('立式钢琴', 'Kawai', 'KU-S10', 'KP2024002', 'available', '2024-02-15', 32000.00, NULL),
('小提琴', 'Suzuki', 'No.280', 'VN2024001', 'available', '2024-03-01', 2800.00, '教学用琴'),
('古筝', '敦煌', '694KK', 'GZ2024001', 'repair', '2023-06-20', 5600.00, '琴码需维修');

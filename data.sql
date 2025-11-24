INSERT INTO public.users (user_id, u_email, u_name, u_surname, u_city, u_phone_number, u_profile_descr, u_password)
VALUES (1, 'arman@mail.com', 'Arman', 'Armanov', 'Astana', '+77001234567', 'Experienced caregiver for elderly people', 'pass123'),
(2, 'amina@mail.com', 'Amina', 'Aminova', 'Almaty', '+77007654321', 'Looking for caregivers for my father', 'pass456'),
(3, 'bek@mail.com', 'Bek', 'Bekov', 'Astana', '+77001112233', 'Playmate for children', 'pass789'),
(4, 'dina@mail.com', 'Dina', 'Dinaeva', 'Astana', '+77002223344', 'Babysitter with 5 years experience', 'pass321');

INSERT INTO public.caregivers (caregiver_id, c_photo, c_gender, c_care_type, c_hourly_rate)
VALUES (1, '/photos/arman.jpg', 'male', 'elder', 12.50),
(3, '/photos/bek.jpg', 'male', 'playmate', 9.50),
(4, '/photos/dina.jpg', 'female', 'babysitter', 15.00);

INSERT INTO public.members (member_id, m_house_rules, m_depend_descr)
VALUES (2, 'No pets. Keep house clean.', 'My 70-year-old father requires daily care');

INSERT INTO public.addresses (a_member_id, a_house_number, a_street, a_town)
VALUES (2, 12, 'Kabanbay Batyr', 'Almaty');

INSERT INTO public.jobs (job_id, j_member_id, j_care_type, j_reqs, j_date_post)
VALUES (1, 2, 'elder', 'Soft-spoken, experienced in elderly care, 09:00-12:00 daily', '2025-11-10'),
(2, 2, 'playmate', 'Creative play activities, 15:00-18:00 weekends', '2025-11-11');

INSERT INTO public.job_applications (ja_caregiver_id, ja_job_id, ja_date_applied)
VALUES (1, 1, '2025-11-12'),
(3, 2, '2025-11-12'),
(4, 2, '2025-11-13');

INSERT INTO public.appointments (appointment_id, ap_caregiver_id, ap_member_id, ap_date, ap_time, ap_work_hours, ap_status)
VALUES (1, 1, 2, '2025-11-15', '09:00', 3.00, 'accepted'),
(2, 4, 2, '2025-11-16', '15:00', 3.00, 'pending');


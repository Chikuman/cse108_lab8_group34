from data_structures import User, Student, Teacher, Class, Enrollment, db

def mockData():
    if not User.query.first():

        u1 = User(username="alice", name='Alice Glass', password="123456")
        u2 = User(username="bob", name='Bob Dylan',password="123456")
        u3 = User(username="tanya",name="Tanya Haden", password="123456")
        u4 = User(username="lily", name= "Lily Collins",password="123456")
        u5 = User(username="carrie", name="Carrie Fisher", password="123456")
        u6 = User(username="ahepworth", name= "Ammon Hepworth", password="iamteacher")
        u7 = User(username="smithyoo", name= "Smith Yoon", password="iamteacher")

        admin_user = User(username="admin", password="admin123", is_admin=True)

        db.session.add_all([u1, u2, u3, u4, u5, u6, u7, admin_user])
        db.session.commit()

        s1 = Student(user_id=u1.id)
        s2 = Student(user_id=u2.id)
        s3 = Student(user_id=u3.id)
        s4 = Student(user_id=u4.id)
        s5 = Student(user_id=u5.id)

        t1 = Teacher(user_id=u6.id)
        t2 = Teacher(user_id=u7.id)

        db.session.add_all([s1, s2, s3, s4, s5, t1, t2])
        db.session.commit()

        c1 = Class(
            class_name="CSE 108",
            class_time="Monday, Wednesday, Friday @ 9:00 AM",
            class_capacity=30,
            teacher_id=t1.teacher_id
        )

        c2 = Class(
            class_name="ENGR 065",
            class_time="Tuesday, Thursday @ 11:00 AM",
            class_capacity=25,
            teacher_id=t1.teacher_id
        )

        c3 = Class(
            class_name="MATH 144",
            class_time="Tuesday, Thursday @ 3:00 PM",
            class_capacity=25,
            teacher_id=t2.teacher_id
        )

        db.session.add_all([c1, c2, c3])
        db.session.commit()

        e1 = Enrollment(student_id=s1.student_id, class_id=c1.class_id)
        e2 = Enrollment(student_id=s2.student_id, class_id=c1.class_id)
        e3 = Enrollment(student_id=s1.student_id, class_id=c2.class_id)
        e4 = Enrollment(student_id=s3.student_id, class_id=c2.class_id)
        e5 = Enrollment(student_id=s4.student_id, class_id=c2.class_id)
        e6 = Enrollment(student_id=s2.student_id, class_id=c3.class_id)
        e7 = Enrollment(student_id=s4.student_id, class_id=c3.class_id)
        e8 = Enrollment(student_id=s5.student_id, class_id=c3.class_id)
        e9 = Enrollment(student_id=s3.student_id, class_id=c1.class_id)

        db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9])
        db.session.commit()
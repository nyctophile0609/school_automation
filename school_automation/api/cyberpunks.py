from .models import *
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.db.models import Q
import calendar


def algorithm_1(days: list, start_date, end_date):
    result1 = {}
    result2 = 0
    for i in days:
        weekday_to_count = i
        count = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == weekday_to_count:
                count += 1
            current_date += timedelta(days=1)
        result2 += count
        result1[i] = count
    return [result1, result2]


def algorithm_2(days: list, start_date: datetime, end_date: datetime):
    result1 = {}
    result2 = []
    print(start_date)
    for weekday in days:
        current_date = start_date
        dates = []
        while current_date <= end_date:
            if current_date.weekday() == weekday:
                dates.append(current_date)
            current_date += timedelta(days=1)

        result1[weekday] = dates
        result2.extend(dates)
    return [result1, result2]


def algorithm_3(year):
    days = [0]
    for month in range(1, 13):
        _, num_days = calendar.monthrange(year, month)
        days.append(num_days)
    return days


def algorithm_4(holidays, lesson_days, start_date, end_date):
    lesson_dates = algorithm_2(lesson_days, start_date=start_date, end_date=end_date)
    print("a-4 result of a-2",lesson_dates)
    lesson_dates = lesson_dates[1]
    x = len(lesson_dates)
    if x != 0:
        for lesson_date in lesson_dates:
            for holiday in holidays:
                if holiday.start_date <= lesson_date <= holiday.end_date:
                    x -= 1
    return x


def student_debt_1(student):
    groups = student.groups.all().exclude(status=False)
    student_discounts = student.student_discounts.all()
    current_date = datetime.now().date()

    print("Current date:", current_date)

    for group in groups:
        if group.start_date <= current_date:
            print("\nProcessing group:", group)
            ps_date = current_date
            pe2 = current_date.month
            pe1 = current_date.year
            if group.start_date.day <= current_date.day:
                if current_date.month != 12:
                    pe2 += 1
                else:
                    pe2 = 1
                    pe1 += 1
            pe_date = date(pe1, pe2, group.start_date.day)
            print("Period start date (ps_date):", ps_date)
            print("Period end date (pe_date):", pe_date)
            payment_object = StudentPaymentModel.objects.filter(
                group=group, student=student, till_date=pe_date
            ).first()
            if payment_object:
                ps_date=payment_object.from_date
            holiday_objects = HolidayModel.objects.filter(
                groups=group, start_date__lte=pe_date, end_date__gte=ps_date
            )
            print("Holiday objects:", holiday_objects)

            lesson = group.lesson
            lesson_price = lesson.price
            discount = lesson.discount
            print("Initial lesson price:", lesson_price)
            print("Lesson discount:", discount)

            lesson_days_queryset = GroupScheduleModel.objects.filter(group=group)
            for i in lesson_days_queryset:
                print(i)
                print(i.id)
                print(i.day)
                print()
            print(lesson_days_queryset)
            lesson_days = [int(u.day) for u in lesson_days_queryset]
            print("Lesson days:", lesson_days)

            flag = [0, []]
            if discount and discount.start_date <= current_date <= discount.end_date:
                lesson_price -= lesson_price * discount.discount_percent / 100
                flag[0] = 1
                print("Applied lesson discount, new lesson price:", lesson_price)

            for student_discount in student_discounts:
                if (
                    student_discount.start_date
                    <= current_date
                    <= student_discount.end_date
                ):
                    flag.append(student_discount)
                    lesson_price -= (
                        lesson_price * student_discount.discount_percent / 100
                    )
                    print("Applied student discount, new lesson price:", lesson_price)

            lesson_price = max(0, lesson_price)
            print("Final lesson price after discounts:", lesson_price)

            qw1 = algorithm_4(holiday_objects, lesson_days, ps_date, pe_date)
            qw2 = algorithm_1(lesson_days, ps_date, pe_date)[1]
            print("Algorithm 4 result (qw1):", qw1)
            print("Algorithm 1 result (qw2):", qw2)

            lesson_price = (lesson_price / max(qw1, 1)) * qw2
            print("Adjusted lesson price based on algorithms:", lesson_price)


            old_payment_amount = 0
            if payment_object:
                print("payment_object exists")
                if payment_object.closed==False:
                    old_payment_amount = payment_object.total_payment
                    payment_object.total_payment = lesson_price
                    payment_object.all_discounts.clear()
                    payment_object.save()
                    print("Updated existing payment object with new lesson price:", lesson_price)
            else:
                payment_object = StudentPaymentModel.objects.create(
                    student=student,
                    group=group,
                    total_payment=lesson_price,
                    from_date=ps_date,
                    till_date=pe_date,
                )
                print("Created new payment object with lesson price:", lesson_price)

            if flag[0]:
                payment_object.all_discounts.add(discount)
            if flag[1]:
                for i in flag[1]:
                    payment_object.all_discounts.add(i)
            payment_object.save()
            print("Saved payment object:", payment_object)

            student.debt -=payment_object.total_payment-old_payment_amount
            print(old_payment_amount,payment_object.total_payment)
            print("Updated student debt, new debt:", student.debt)
            student.save()

    return True


def student_debt_2(student, group):
    student_discounts = student.student_discounts.all()
    current_date = datetime.now().date()
    if group.start_date >= current_date:
        pe_date = current_date
        ps2 = current_date.month
        ps1 = current_date.year
        if group.start_date.day <= current_date.day:
            if current_date.month != 1:
                ps2 -= 1
            else:
                ps2 = 12
                ps1 -= 1
        ps_date = date(ps1, ps2, group.start_date.day)

        payment_object = StudentPaymentModel.objects.filter(
            group=group, student=student, from_date__gte=ps_date
        ).first()

        discount_date = (
            payment_object.paid_date
            if payment_object
            and payment_object.total_payment + payment_object.paid_payment == 0
            else current_date
        )
        holiday_objects = HolidayModel.objects.filter(
            groups=group, start_date__lte=pe_date, end_date__gte=ps_date
        )

        lesson = group.lesson
        lesson_price = lesson.price
        discount = lesson.discount
        lesson_days_queryset = GroupScheduleModel.objects.values("day").filter( 
            group=group
        )
        lesson_days = [int(_["day"]) for _ in lesson_days_queryset]

        flag = [0, []]
        if discount and discount.start_date <= discount_date <= discount.end_date:
            lesson_price -= lesson_price * discount.discount_percent / 100
            flag[0] = 1
        for student_discount in student_discounts:
            if (
                student_discount.start_date
                <= discount_date
                <= student_discount.end_date
            ):
                flag.append(student_discount)
                lesson_price -= lesson_price * student_discounts.discount_percent / 100
        lesson_price = max(0, lesson_price)

        qw1 = algorithm_4(holiday_objects, lesson_days, ps_date, pe_date)
        qw2 = algorithm_1(lesson_days, ps_date, pe_date)[1]
        lesson_price = (lesson_price / qw1) * qw2
        old_payment_amount = 0
        if payment_object:
            old_payment_amount = payment_object.total_payment
            payment_object.total_payment = lesson_price
            payment_object.from_date = ps_date
            payment_object.till_date = pe_date
            payment_object.all_discounts.clear()
        else:
            payment_object = StudentPaymentModel.objects.create(
                student=student,
                group=group,
                total_payment=lesson_price,
                from_date=ps_date,
                till_date=pe_date,
            )
        if flag[0]:
            payment_object.all_discounts.add(discount)
        if flag[1]:
            for i in flag[1]:
                payment_object.all_discounts.add(i)
        payment_object.save()
        student.debt -=payment_object.total_payment-old_payment_amount
        return True


def teachers_salary_1(teacher,):
    current_date = datetime.now().date()
    ss_date = date(current_date.year, current_date.month, 1)
    se1, se2 = (
        ss_date.month != 12
        and [current_date.year, current_date.month + 1]
        or [current_date.year + 1, 1]
    )
    se_date = date(se1, se2, 1)
    # if TeacherSalaryModel.objects.filter``
    if teacher.salary_type == "fixed_salary":
        salary_object = TeacherSalaryModel.objects.filter(
            teacher=teacher, till_date__lte=se_date, till_date__gte=ss_date
        )
        if salary_object:
            return salary_object
        else:
            days = algorithm_3(current_date.year)
            monthly_salary = (teacher.commission / days[current_date.month]) * (
                se_date - current_date
            ).days
            salary_object = TeacherSalaryModel.objects.create(
                teacher=teacher,
                total_payment=monthly_salary,
                group=None,
                total=True,
                from_date=current_date,
                till_date=se_date,
            )
            return salary_object

    elif teacher.salary_type == "commission_based_salary":
        groups =GroupModel.objects.filter(teacher=teacher)
        total_salary = 0
        for group in groups:
            payments = StudentPaymentModel.objects.filter(
                Q(group=group)
                & (
                    Q(till_date__range=(ss_date, se_date))
                    | Q(from_date__range=(ss_date, se_date))
                )
            ).distinct()
            holiday_objects = HolidayModel.objects.filter(
                Q(groups=group)
                & (
                    Q(start_date__range=(ss_date, se_date))
                    | Q(end_date__range=(ss_date, se_date))
                )
            )

            gt_payment = 0
            lesson_days_queryset = GroupScheduleModel.objects.values("day").filter(
                group=group
            )
            lesson_days = [_["day"] for _ in lesson_days_queryset]
            for payment in payments:
                qw3 = 0
                qw1 = algorithm_4(
                    holiday_objects, lesson_days, payment.from_date, payment.till_date
                )
                qw2 = algorithm_4(
                    holiday_objects,
                    lesson_days,
                    max(payment.from_date, ss_date),
                    min(payment.till_date, se_date),
                )
                qw3 = (payment.total_payment / qw1) * qw2
                gt_payment += qw3
            if TeacherSalaryModel.objects.filter(
                teacher=teacher,
                group=group,
                till_date__lte=se_date,
                from_date__gte=ss_date,
            ):
                salary_object = TeacherSalaryModel.objects.filter(
                    teacher=teacher,
                    group=group,
                    till_date__lte=se_date,
                    from_date__gte=ss_date,
                )
                salary_object.total_payment = gt_payment
                salary_object.save()
            else:
                salary_payment = TeacherSalaryModel.objects.create(
                    teacher=teacher,
                    total_payment=gt_payment,
                    group=group,
                    from_date=ss_date,
                    till_date=se_date,
                )
            total_salary += gt_payment

        salary_object = TeacherSalaryModel.objects.filter(
            teacher=teacher, till_date__lte=se_date, from_date__gte=ss_date, total=True
        ).first()
        if salary_object:
            salary_object.total_payment = total_salary
            salary_object.save()
        else:
            salary_object = TeacherSalaryModel.objects.create(
                teacher=teacher,
                total_payment=total_salary,
                group=None,
                from_date=ss_date,
                till_date=se_date,
                total=True,
            )
    return True


def teachers_salary_2(teacher, group):
    print("11111111111111111111111")
    current_date = datetime.now().date()
    salary_object = TeacherSalaryModel.objects.get_or_create(
        till_date__lte=current_date, group=group, teacher=teacher
    )
    ss_date = salary_object.from_date
    se_date = current_date
    print("11111111111111111111111")
    total_salary_object = TeacherSalaryModel.objects.get_or_create(
        till_date__lte=se_date, teacher=teacher, total=True
    )
    print("11111111111111111111111")


    if teacher.salary_type == "fixed_salary":
        if total_salary_object:
            days = algorithm_3(current_date.year)
            monthly_salary = (teacher.commission / days[current_date.month]) * (
                current_date - salary_object.from_date
            ).days 
            total_salary_object.total_payment = monthly_salary
            total_salary_object.till_date = current_date
            total_salary_object.save()
            return total_salary_object
        else:
            days = algorithm_3(current_date.year)
            monthly_salary = (teacher.commission / days[current_date.month]) * (
                current_date - ss_date
            ).days
            total_salary_object = TeacherSalaryModel.objects.create(
                teacher=teacher,
                total_payment=monthly_salary,
                group=None,
                total=True,
                from_date=ss_date,
                till_date=current_date,
            )
            return total_salary_object
    elif teacher.salary_type == "commission_based_salary":
        lesson_days_queryset = GroupScheduleModel.objects.values("day").filter(
            group=group
        )
        lesson_days = [_["day"] for _ in lesson_days_queryset]

        payments = StudentPaymentModel.objects.filter(
            Q(group=group)
            & (
                Q(till_date__range=(ss_date, se_date))
                | Q(from_date__range=(ss_date, se_date))
            )
        ).distinct()

        holiday_objects = HolidayModel.objects.filter(
            Q(groups=group)
            & (
                Q(start_date__range=(ss_date, se_date))
                | Q(end_date__range=(ss_date, se_date))
            )
        )
        gt_payment = 0
        for payment in payments:
            qw3 = 0
            qw1 = algorithm_4(
                holiday_objects, lesson_days, payment.from_date, payment.till_date
            )
            qw2 = algorithm_4(
                holiday_objects,
                lesson_days,
                max(payment.from_date, ss_date),
                min(payment.till_date, se_date),
            )
            qw3 = (payment.total_payment / qw1) * qw2
            gt_payment += qw3
        total_salary_object.total_payment -= salary_object.total_payment
        salary_object.total_payment = gt_payment
        total_salary_object.total_payment += gt_payment
        salary_object.save()
        total_salary_object.save()
        return total_salary_object


def staff_user_1(staff_user):


    current_date = datetime.now().date()
    
    ss_date = date(current_date.year, current_date.month, 1)
    
    se1, se2 = (
        ss_date.month != 12
        and [current_date.year, current_date.month + 1]
        or [current_date.year + 1, 1]
    )
    se_date = date(se1, se2, 1)

    salary_object = StaffUserSalaryModel.objects.filter(
        staff_user=staff_user, till_date__lte=se_date, till_date__gte=ss_date
    ).first()
    print(salary_object)
    days = algorithm_3(current_date.year)
    if salary_object and salary_object.closed:
        return salary_object

    if salary_object==None:
        print(1.1)
        total_salary = (staff_user.salary / days[current_date.month]) * (
            se_date - current_date
        ).days
        salary_object = StaffUserSalaryModel.objects.create(
            staff_user=staff_user,
            total_payment=total_salary,
            from_date=current_date,
            till_date=se_date,  
        )
    else:
        total_salary = (staff_user.salary / days[current_date.month]) * (
        salary_object.till_date - salary_object.from_date).days
        salary_object.total_payment=total_salary
        salary_object.save()
        print(total_salary,salary_object.total_payment)

    return salary_object






# def staff_user_2(staff_user):

#     current_date = datetime.now().date()
    
#     ss_date = date(current_date.year, current_date.month, 1)
    
#     se1, se2 = (
#         ss_date.month != 12
#         and [current_date.year, current_date.month + 1]
#         or [current_date.year + 1, 1]
#     )
#     se_date = date(se1, se2, 1)
#     salary_object = StaffUserSalaryModel.objects.filter(staff_user=staff_user, till_date__lte=se_date, till_date__gte=ss_date).first()
#     days = algorithm_3(current_date.year)


#     if salary_object:
#         total_salary = (staff_user.salary / days[current_date.month]) * (
#         salary_object.till_date - salary_object.from_date).days
#         salary_object
#     else:
#         total_salary = (staff_user.salary / days[current_date.month]) * (
#         se_date - current_date).days
#         salary_object=StaffUserSalaryModel.objects.create(
#             staff_user=staff_user,
#             from_date=current_date,
#             till_date=se_date,
#             total_payment=total_salary)
        

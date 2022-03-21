$(document).ready(function(jQuery) {
    jQuery(function ($) {
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let summa_field = $('input#id_summa');
        summa_field.attr('disabled', true);
        let cost_field = $('input#id_cost');
        cost_field.attr('disabled', true);
        let date_start = $('input#id_datestart');
        let time_start = $('input#id_timestart');
        let service_field = $('select#id_service');
        let services = service_field.val();
        date_start.attr('disabled', true);
        time_start.attr('disabled', true);
        let mcid = id_mcid.value;
        let doctor = id_doctor.value;
        let scheduleid = id_scheduleid.value;
        let scheduletext = $( "#id_scheduleid option:selected" ).text();
        let isStaff = false;
        let exempttype = '';
        let exempt = 0;
        let cost = 0;
        let summa = 0;
        let schedule = new Array();
        let opt=$('select#id_scheduleid');
        let editing = false;
        let url = $(location).attr('href')


        // MEDCARD CATCHING
        get_medcard().then(function(response){
                console.log(response);
                editing = true
                // console.log(editing)
                // let schedule_temp = id_scheduleid.value;
            }).catch(function (err){
                opt.html('');
                opt.append($('<option value selected>---------</option>'))
                console.log('Пациент не найден');
            });

        document.querySelector('select[name="mcid"]').onchange=function() {
            mcid = id_mcid.value
            console.log('Идентификатор медицинской карты: ' + id_mcid.value)
            get_medcard().then(function(response){
                console.log(response);
                summa_calc()
            }).catch(function (err){
                console.log('Пациент не найден');
            });
        };

        function get_medcard(){
            return new Promise(function (resolve, reject){
                $.ajax({
                    type: "POST",
                    url: "{{ '../../../../../../../get_medcard' }}",
                    data: { csrfmiddlewaretoken: csrftoken, text: mcid },
                    success: function callback(response){
                                console.log('patient connection successful; response is: ' + response);
                                response = JSON.parse(response);
                                isStaff = response['isStaff'];
                                exempttype = response['exempttype'];
                                exempt = response['exempt'];
                                if (isStaff){
                                    alert("Пациент являет сотрудником компании, поэтому лечение пройдет бесплатно")
                                    id_summa.value = 0
                                } else {
                                    if (exempttype === ''){
                                        alert('У пациента нет льгот, скидка не предоставляется')
                                    } else {
                                        alert('Пациент является: ' + exempttype + '. На услуги предоставляется скидка в размере: ' + exempt )
                                    }
                                }
                                // summa_calculation()
                                resolve('Данные пациента загружены')
                    },
                    error: function (err) {
                        reject('Пациент не найден')
                    }
                })
            })
        }


        // SCHEDULE CATCHING
        get_schedule().then(function(response){
                console.log(response);
                schedule_edit();
            }).catch(function (err){
                console.log('Доктор не найден. Ошибка: ' + err);
            });

        document.querySelector('select[name="doctor"]').onchange=function() {
            doctor = id_doctor.value
            console.log('Идентификатор доктора: ' + id_doctor.value)
            get_schedule().then(function(response){
                console.log(response);
                schedule_edit();
            }).catch(function (err){
                console.log('Доктор не найден. Ошибка: ' + err);
            });
        };

        function get_schedule(){
            return new Promise(function (resolve, reject){
                $.ajax({
                    type: "POST",
                    url: "{{ '../../../../../../../get_schedule' }}",
                    data: { csrfmiddlewaretoken: csrftoken, text: doctor, 'link': url, 'editing': editing},
                    success: function callback(response){
                                console.log('schedule connection successful; response is: ' + response);
                                schedule = JSON.parse(response);
                                console.log(schedule)
                                resolve('Данные доктора загружены')
                    },
                    error: function (err) {
                        reject('Доктор не найден')
                    }
                })
            })
        }

        function schedule_edit(){
            opt.html('');
            opt.append($('<option value selected>---------</option>'))
            console.log(schedule)
            $.each(schedule,function(key,data) {
                console.log('Ответ: ' + key);
                $.each(data, function (index, value) {
                    console.log('Запись: id = ' + value['schedule_id'] + '; Название = '+ value['schedule']);
                    opt.append($('<option/>').val(value['schedule_id']).text(value['schedule']));
                });
            });
            if (editing){
                console.log(scheduletext)
                $('#id_scheduleid option:contains("' + scheduletext + '")').attr('selected', true);
            }
        }

        // CHANGE DATE & TIME AT SCHEDULE SELECTING
        opt.on('change', function() {
             console.log(id_scheduleid.value);
             scheduleid = id_scheduleid.value;
             get_record().then(function(data){
                console.log(data)
             }).catch(function (err){
                console.log(err)
             })
        });

        function get_record(){
            return new Promise(function (resolve, reject){
                $.ajax({
                    type: "POST",
                    url: "{{ '../../../../../../../get_record' }}",
                    data: { csrfmiddlewaretoken: csrftoken, text: scheduleid },
                    success: function callback(response){
                                console.log('server connection successful; response is: ' + response);
                                response = JSON.parse(response);
                                id_datestart.value = response['date'];
                                id_timestart.value = response['start_time']
                                resolve('Данные о времени приема загружены')
                    },
                    error: function (err) {
                        reject('Данные о времени приема не найдены')
                    }
                });
            });
        }

        //RECEIVING DATA ON COST OF SERVICES AND SUMMARIZE THEM
        service_field.on('change', function() {
            services = service_field.val()
            get_cost().then(function(data){
               console.log(data)
                summa_calc()
            }).catch(function (err){
               console.log(err)
            })
        });

        function get_cost(){
            return new Promise(function (resolve, reject){
                services = JSON.stringify(services)
                $.ajax({
                    type: "POST",
                    url: "{{ '../../../../../../../get_cost' }}",
                    data: { csrfmiddlewaretoken: csrftoken, text: services },
                    success: function callback(response){
                                console.log('server connection successful; response is: ' + response);
                                response = JSON.parse(response);
                                cost = response['cost']
                                id_cost.value = cost
                                resolve('Данные о стоимости услуг загружены')
                    },
                    error: function (err) {
                        reject('Данные о стоимости услуг не найдены')
                    }
                });
            });
        }

        function summa_calc(){
            if (isStaff){
                id_summa.value = 0;
            } else {
                summa = cost - exempt
                if (summa < 0){
                    id_summa.value = 0;
                } else {
                    id_summa.value = summa;
                }
            }
        }

        //SAVING OBJECT AND BLOCKING SCHEDULE RECORD IN DB
        let frm = $('form');
        let chosenBtn = frm.find('[name="_save"]');
        let btns = frm.find('[name="_save"], [name="_addanother"], [name="_continue"]');
        btns.unbind('click.btnAssign').bind('click.btnAssign', function(e)
        {
            chosenBtn = $(this);
        });
        frm.unbind('submit.saveStuff').bind('submit.saveStuff', function(e)
        {

            cost_field.attr("disabled", false);
            summa_field.attr("disabled", false);
            date_start.attr('disabled', false);
            time_start.attr('disabled', false);
            change_schedule().then(function(response){
                console.log(response);
            }).catch(function (err){
                console.log('При сохранении произошла ошибка: ' + err);
            });

            frm.append(
            [
                '<input type="hidden" name="',
                chosenBtn.attr('name'),
                '" value="',
                chosenBtn.attr('value'),
                '" />'
            ].join(''));
        });

        function change_schedule(){
            return new Promise(function (resolve, reject){
                $.ajax({
                    type: "POST",
                    url: "{{ '../../../../../../../change_schedule' }}",
                    data: { csrfmiddlewaretoken: csrftoken, text: scheduleid },
                    success: function callback(response){
                                console.log('server connection successful; response is: ' + response);
                                resolve('Данные о расписании доктора изменены')
                    },
                    error: function (err) {
                        reject('Данные о расписании не изменены')
                    }
                });
            });
        }
    });
});
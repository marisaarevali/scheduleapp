#!/usr/bin/python
# -*- coding: utf-8 -*-



from flask import Flask, render_template, request, redirect, url_for, flash
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL



app=Flask(__name__,template_folder='template')
app.secret_key = 'super secret'


app.config['MYSQL_HOST'] = 'your_ip'
app.config['MYSQL_USER'] = 'mysql_user'
app.config['MYSQL_PASSWORD'] = 'mysql_password'
#juhul kui kasutada algset lehte, kus saab sisestada andmebaasi (testimiseks), siis kasutada messageboard
#app.config['MYSQL_DB'] = 'messageboard'
app.config['MYSQL_DB'] = 'database_name'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

el_nadalapaev = [
    "Esmaspaev",
    "Teisipaev",
    "Kolmapaev",
    "Neljapaev",
    "Reede",
    "Laupaev",
    "Puhapaev"]

el_aeg = [
"08:00",
"08:30",
"09:00",
"09:30",
"10:00",
"10:30",
"11:00",
"11:30",
"12:00",
"12:30",
"13:00",
"13:30",
"14:00",
"14:30",
"15:00",
"15:30",
"16:00",
"16:30",
"17:00",
"17:30",
"18:00",
"18:30",
"19:00",
"19:30",
"20:00",
"20:30",
"21:00",
"21:30",
"22:00"]

el_weekdays = [
"08:00 - 08:30",
"08:30 - 09:00",
"09:00 - 09:30",
"09:30 - 10:00",
"10:00 - 10:30",
"10:30 - 11:00",
"11:00 - 11:30",
"11:30 - 12:00",
"12:00 - 12:30",
"12:30 - 13:00",
"13:00 - 13:30",
"13:30 - 14:00",
"14:00 - 14:30",
"14:30 - 15:00",
"15:00 - 15:30",
"15:30 - 16:00",
"16:00 - 16:30",
"16:30 - 17:00",
"17:00 - 17:30",
"17:30 - 18:00",
"18:00 - 18:30",
"18:30 - 19:00",
"19:00 - 19:30",
"19:30 - 20:00",
"20:00 - 20:30",
"20:30 - 21:00",
"21:00 - 21:30",
"21:30 - 22:00"]

# @app.route('/dfhdfghdtutr456745323rdswDeDsE/<string:value>', methods = ['GET'])
# def delete(value):
#     print(value)
#     cur = mysql.connection.cursor()
#     cur.execute("UPDATE treener SET name =%s , phone = %s, email = %s status = %s WHERE id = %s, (nimi,telefon,email,staatus,value,))
#     mysql.connection.commit()
#     return redirect(url_for('treening'))

@app.route('/lk2343RRRRhfgdsawret2kfo4ETDDHJJFD2/<string:value>', methods = ['GET'])
def delete(value):
    ##flash("Record Has Been Deleted Successfully ")
    #print(value)
    cur = mysql.connection.cursor()
    #cur.execute("DELETE FROM graafik WHERE id=%s", (value,))
    cur.execute("DELETE FROM graafik WHERE id={}".format(value))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('treening'))


@app.route('/grupilisamine', methods=['GET', 'POST'])
def grupilisamine():

    query_opilased = 'select * from opilane where status=1'
    query_hooaeg = 'select max(id) from hooaeg'
    query_grupp = 'select max(id) from grupp'

    cur = mysql.connection.cursor()
    
    cur.execute(query_opilased)
    data_opilased = cur.fetchall()

    cur.execute(query_hooaeg)
    data_hooaeg = cur.fetchall()

    cur.execute(query_grupp)
    data_grupp = cur.fetchall()
    

    #print(data_opilased)
    praegune_hooaeg = data_hooaeg[0][0]
    praegune_grupi_id = data_grupp[0][0]
    opilased = []
    opilased2 = []
    uus_grupi_id = praegune_grupi_id + 1
    if request.method == "POST":
        ## võta kasutaja sisestatud muudetud andmed
        details = request.form
        details2 = request.form.getlist
        nimi = details['nimi']
        opilased = details2('opilased')
        #print(nimi)
        #print(opilased)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO grupp(name,hooaeg_id) VALUES ('{}',{})".format(nimi,praegune_hooaeg))
        for i in opilased:
            opilased2.append(int(i))
            print(i)
            print(uus_grupi_id)
            print(praegune_hooaeg)
        for i in opilased2:        
            cur.execute("INSERT INTO grupp_opilane(opilane_id,grupp_id,hooaeg_id) VALUES ({},{},{})".format(i,uus_grupi_id,praegune_hooaeg))
            
            print(uus_grupi_id)
            print(praegune_hooaeg)        
         
        mysql.connection.commit()
        cur.close()  

        return redirect(url_for('grupid'))

    # uue grupi loomise ruoute, Mari jaoks
    
    return render_template('grupilisamine.html', data_opilased=data_opilased)



@app.route('/grupimuudatused/<string:t_id>', methods=['GET', 'POST'])
def grupimuudatused(t_id):
    #print(t_id)
    cur = mysql.connection.cursor()   

    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()    
    hooaeg_praegu = hooaeg_max[0][0]
    
    query_opilane ='select opilane.id,opilane.name from opilane where status=1'
    query_grupp = 'select * from grupp where hooaeg_id={}'.format(hooaeg_praegu)

    cur.execute(query_grupp)
    data_grupp = cur.fetchall()

    cur.execute(query_opilane)
    data_opilane = cur.fetchall()

    opilane_list = [list(row) for row in data_opilane] # list of lists
    #print(opilane_list)

    ## grupi id mida muudame
    for row in data_grupp:
        if row[1] == t_id:
            grupp_id = row[0]
            #print(grupp_id)
    

    # õpilaste id kes on muudetavas grupis
    query_grupp_opilane = 'select grupp_opilane.opilane_id from grupp_opilane where grupp_id={}'.format(grupp_id)
    cur.execute(query_grupp_opilane)
    data_grupp_opilane = cur.fetchall()
    #print(data_grupp_opilane)
    ## õpilaste id kes on muudetavas grupis LISTINA
    data_grupp_opilane_m = []
    grupis_olemas = []    
    for row in data_grupp_opilane:
        data_grupp_opilane_m.append(row[0])
        #kui valitud õpilase id == data_opilane[0] siis pane checked
        for i in opilane_list:            
            if i[0] == row[0]:
                grupis_olemas.append(i)
                opilane_list.remove(i)
    
    opilased = []
    opilased2 = []
    
    if request.method == "POST":
        ## võta kasutaja sisestatud muudetud andmed
        details = request.form
        details2 = request.form.getlist
        nimi = details['nimi']
        opilased = details2('opilased')
        print(nimi)
        #print(opilased)
        cur = mysql.connection.cursor()
        cur.execute("delete from grupp_opilane where grupp_id={}".format(grupp_id))
        for i in opilased:
            opilased2.append(int(i))
            print(opilased2)        

        for i in opilased2:
            cur.execute("INSERT INTO grupp_opilane(opilane_id,grupp_id,hooaeg_id) VALUES ({}, {}, {})".format(i,grupp_id,hooaeg_praegu))
            cur.execute("update grupp set name='{}' where id={}".format(nimi,grupp_id))
        #print(uus_grupi_id)
        #print(praegune_hooaeg)        
         
        mysql.connection.commit()
        return redirect(url_for('grupid'))   
 



    return render_template("grupimuudatused.html",grupis_olemas=grupis_olemas,opilane_list=opilane_list, t_id=t_id,data_opilane=data_opilane)



@app.route('/gruppkopeeri', methods=['GET', 'POST'])
def gruppkopeeri():


    query_grupp = 'select * from grupp'
    cur = mysql.connection.cursor()

    cur.execute(query_grupp)
    data_grupp = cur.fetchall() 

    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]


    
    eelnevad_grupid = []    
    grupi_idd = []
    # lisame eelnevad_grupid listi grupi nimed ja grupi_id_d listi, gruppide id-d. Viimast teeme selleks, et teada saada,
    # mis on kõige suurem ID gruppide tabelis, lisatav grupp on sellest yhe v6rra suurem
    for i in data_grupp:
        eelnevad_grupid.append(i[1])
        grupi_idd.append(i[0])
        
    lisatava_grupi_id = max(grupi_idd) + 1

    if request.method == "POST":
        ## võta kasutaja sisestatud muudetud andmed
        details = request.form
        grupi_nimi = details['nimi']
        grupp_to_copy = details['vana_grupp']
        
        print(grupi_nimi)
        print(grupp_to_copy) 
            
        print(data_grupp)       

        cpy_grp_id = 0
        # j2rnevalt saame teada, kopeeritava grupi ID
        for num ,i in enumerate(data_grupp):
            if grupp_to_copy == i[1]:
                cpy_grp_id = data_grupp[num][0]
                
        print(type(cpy_grp_id))
        query_op_idd = 'select opilane_id from grupp_opilane where grupp_id={}'.format(cpy_grp_id)
        cur.execute(query_op_idd)
        data_idd = cur.fetchall() 
        print(data_idd)
        print(len(data_idd))

        # votame opilaste id-d tuplest v2lja ja paneme listi:
        idd = []
        if len(data_idd) > 0:

            for p in data_idd:
                for m in p:
                    idd.append(m)
                        
            # loome gupp tabelisse uue sissekande:
            try:
                create_grupp_query = "INSERT INTO grupp(name,hooaeg_id) VALUES ('{}',{})".format(grupi_nimi,hooaeg_praegu)
                cur.execute(create_grupp_query)


                for e in idd:
                    insert_query = 'INSERT INTO grupp_opilane(opilane_id,grupp_id,hooaeg_id) VALUES ({},{},{})'.format(e,lisatava_grupi_id,hooaeg_praegu)
                    cur.execute(insert_query)
            
                mysql.connection.commit()
            except:
                return 'Tekkis probleem uue grupi loomisel'


        else:
            cur.close()
            return('Viga! Valitud grupis pole õpilasi')
        
        cur.close()
        return redirect(url_for('grupid')) 

    cur.close()
    return render_template('gruppkopeeri.html',eelnevad_grupid=eelnevad_grupid)




@app.route('/treenerimuudatused/<string:t_id>', methods=['GET', 'POST'])
def treenerimuudatused(t_id):
    print(t_id)
    query_treener_m = 'select * from treener where id={}'.format(t_id)
    cur = mysql.connection.cursor()
    
    cur.execute(query_treener_m)
    data_treener_m = cur.fetchall()
    # miskip2rast tuple data, mille saame baasist, on tuple inside tuple; tuple len = 1
    # meil on aga vaja et yhes tuples oleks koik olemas, ja et tuple len poleks 1
    if len(data_treener_m) < 3:
        treener_data = data_treener_m[0]
    else:
        treener_data = data_treener_m

    if treener_data[4] == 1:
        el_staatus = ('Aktiivne','Mitte aktiivne')
    else:
        el_staatus = ('Mitte aktiivne','Aktiivne')

    if request.method == "POST":
        ## võta kasutaja sisestatud muudetud andmed
        details = request.form
        nimi = details['nimi']
        telefon = details['telefon']
        email = details['email']
        staatus = details['staatus']

        #print(nimi,telefon,email,staatus)
        
        if staatus == 'Aktiivne':
            loplik_staatus = 1
        else:
            loplik_staatus = 0
    
        try:
            cur = mysql.connection.cursor()
            cur.execute("update treener set name='{}',phone='{}',email='{}',status={} where id={}".format(nimi,telefon,email,loplik_staatus,t_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('treenerid'))
        except:
            return 'Tekkis probleem andmete muutmisel'
        

    else:
        cur.close()
        return render_template("treenerimuudatused.html", t_id=t_id,treener_data=treener_data,el_staatus=el_staatus)




@app.route('/opilasemuudatused/<string:t_id>', methods=['GET', 'POST'])
def opilasemuudatused(t_id):
    print(t_id)
    query_opilane_m = 'select * from opilane where id={}'.format(t_id)
    cur = mysql.connection.cursor()
    
    cur.execute(query_opilane_m)
    data_opilane_m = cur.fetchall()
    # miskip2rast tuple data, mille saame baasist, on tuple inside tuple; tuple len = 1
    # meil on aga vaja et yhes tuples oleks koik olemas, ja et tuple len poleks 1
    if len(data_opilane_m) < 3:
        opilane_data = data_opilane_m[0]
    else:
        opilane_data = data_opilane_m

    if opilane_data[6] == 1:
        el_staatus = ('Aktiivne','Mitte aktiivne')
    else:
        el_staatus = ('Mitte aktiivne','Aktiivne')

    if request.method == "POST":
        ## võta kasutaja sisestatud muudetud andmed
        details = request.form
        nimi = details['nimi']
        aadress = details['aadress']
        regioon = details['regioon']
        telefon = details['telefon']
        email = details['email']
        staatus = details['staatus']

        #print(nimi,telefon,email,staatus)
        
        if staatus == 'Aktiivne':
            loplik_staatus = 1
        else:
            loplik_staatus = 0
    
        try:
            cur = mysql.connection.cursor()
            cur.execute("update opilane set name='{}',address='{}',region='{}',phone='{}',email='{}',status={} where id={}".format(nimi,aadress,regioon,telefon,email,loplik_staatus,t_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('opilased'))
        except:
            return 'Tekkis probleem andmete muutmisel'
        

    else:
        cur.close()
        return render_template("opilasemuudatused.html", t_id=t_id,opilane_data=opilane_data,el_staatus=el_staatus)

@app.route('/saalimuudatused/<string:t_id>', methods=['GET', 'POST'])
def saalimuudatused(t_id):
    print(t_id)
    query_valjak_m = 'select * from valjak where id={}'.format(t_id)
    cur = mysql.connection.cursor()
    
    cur.execute(query_valjak_m)
    data_valjak_m = cur.fetchall()
    # miskip2rast tuple data, mille saame baasist, on tuple inside tuple; tuple len = 1
    # meil on aga vaja et yhes tuples oleks koik olemas, ja et tuple len poleks 1
    if len(data_valjak_m) < 3:
        valjak_data = data_valjak_m[0]
    else:
        valjak_data = data_valjak_m

    if valjak_data[2] == 1:
        el_staatus = ('Aktiivne','Mitte aktiivne')
    else:
        el_staatus = ('Mitte aktiivne','Aktiivne')

    if request.method == "POST":
        ## võta kasutaja sisestatud muudetud andmed
        details = request.form
        nimi = details['nimi']
        staatus = details['staatus']

        #print(nimi,telefon,email,staatus)
        
        if staatus == 'Aktiivne':
            loplik_staatus = 1
        else:
            loplik_staatus = 0
    
        try:
            cur = mysql.connection.cursor()
            cur.execute("update valjak set name='{}',status={} where id={}".format(nimi,loplik_staatus,t_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('treeningsaalid'))
        except:
            return 'Tekkis probleem andmete muutmisel'
        

    else:
        cur.close()
        return render_template("saalimuudatused.html", t_id=t_id,valjak_data=valjak_data,el_staatus=el_staatus)




@app.route('/tasememuudatused/<string:t_id>', methods=['GET', 'POST'])
def tasememuudatused(t_id):
    print(t_id)
    query_tase_m = 'select * from tase where id={}'.format(t_id)
    cur = mysql.connection.cursor()
    
    cur.execute(query_tase_m)
    data_tase_m = cur.fetchall()
    # miskip2rast tuple data, mille saame baasist, on tuple inside tuple; tuple len = 1
    # meil on aga vaja et yhes tuples oleks koik olemas, ja et tuple len poleks 1
    if len(data_tase_m) < 3:
        tase_data = data_tase_m[0]
    else:
        tase_data = data_tase_m

    if tase_data[6] == 1:
        el_staatus = ['Aktiivne','Mitte aktiivne']
    else:
        el_staatus = ['Mitte aktiivne','Aktiivne']

    if request.method == "POST":
        ## võta kasutaja sisestatud muudetud andmed
        details = request.form
        nimi = details['nimi']
        tyyp1 = details['tyyp1']
        tunnid1 = details['tunnid1']
        tyyp2 = details['tyyp2']
        tunnid2 = details['tunnid2']
        staatus = details['staatus']

        print(nimi,tyyp1,tunnid1,tyyp2,tunnid2,staatus)
        
        if staatus == 'Aktiivne':
            loplik_staatus = 1
        else:
            loplik_staatus = 0
    
        try:
            cur = mysql.connection.cursor()
            cur.execute("update tase set name='{}',type1='{}',hours1={},type2='{}',hours2={},status={} where id={}".format(nimi,tyyp1,tunnid1,tyyp2,tunnid2,loplik_staatus,t_id))
            mysql.connection.commit()
            return redirect(url_for('tasemed'))
            cur.close()
        except:
            return (loplik_staatus)
            

    else:
        cur.close()
        return render_template("tasememuudatused.html", t_id=t_id,tase_data=tase_data,el_staatus=el_staatus)


@app.route('/viga1', methods=['GET', 'POST'])
def viga1():
    return render_template('viga1.html')

@app.route('/viga2', methods=['GET', 'POST'])
def viga2():
    return render_template('viga2.html')

@app.route('/viga3', methods=['GET', 'POST'])
def viga3():
    return render_template('viga3.html')





@app.route('/treening', methods=['GET', 'POST'])
def treening():

    cur = mysql.connection.cursor()

    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    
    query_v2ljak = 'select * from valjak where status = 1'
    query_grupp = 'select * from grupp where hooaeg_id = (select max(id) from hooaeg)'
    query_treener = 'select * from treener where status = 1'  
    query_graafik = 'select * from graafik where hooaeg_id = (select max(id) from hooaeg)'
    query_trennid = 'select * from graafik ORDER BY weekday, valjak_id, start_time'
    #query_trennid2 = 'select graafik.id,  graafik.weekday, graafik.valjak_id, graafik.start_time, graafik.end_time, valjak.name as valjakname, grupp.name as gruppname, treener.name as treenername, graafik.t_type from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id order by weekday, valjak_id;' 
    query_trennid2 = "select graafik.id, graafik.weekday, graafik.valjak_id, graafik.start_time, graafik.end_time, valjak.name as valjakname, grupp.name as gruppname, treener.name as treenername, graafik.t_type from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} order by weekday, valjak_id".format(hooaeg_praegu)
    #query_trennid2 = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, grupp.name as gruppname, treener.name as treenername from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} order by weekday, valjak_id".format(hooaeg_praegu)

    query_hooaeg = 'select max(id) from hooaeg'
    
    cur.execute(query_v2ljak)
    data_v2ljak = cur.fetchall() 
         

    cur.execute(query_grupp)
    data_grupp = cur.fetchall()

    cur.execute(query_treener)
    data_treener = cur.fetchall()

    cur.execute(query_graafik)
    #pealkirjad = cur.description ## võta table pealkirjad
    data_graafik = cur.fetchall()

    # martin kommis sisse j2rgmised 2 rida
    cur.execute(query_trennid)
    data_trennid = cur.fetchall()

    cur.execute(query_trennid2)
    data_trennid2 = cur.fetchall()

    cur.execute(query_hooaeg)
    data_hooaeg = cur.fetchall()
    
    cur.close()

    v2ljakud = [] 
    grupid = []  
    grupid_id = []
    treenerid = []
    trennid = []
    #trennid_list = []
    trennid_list2 = []
    treeningtyyp = ['Uldfuusiline','Tennis']

    #print(data_hooaeg)
    #praegune_hooaeg = data_hooaeg[0][0]

    #print(praegune_hooaeg)

    # martin kommis sisse kaks j2rgmist rida:
    for row in list(data_trennid):
        trennid.append(row)
        #if row[1] == 1:
            ##print(trennid)
            #trennid[row[1]] == el_nadalapaev[0]
    
    
    #trennid_list = [list(row) for row in data_trennid] # list of lists

    trennid_list2 = [list(row) for row in data_trennid2] # list of lists
   
    for num, i in enumerate(trennid_list2):
        if i[1] == 1:
            trennid_list2[num][1] = 'Esmaspaev'
        if i[1] == 2:
            trennid_list2[num][1] = 'Teisipaev'
        if i[1] == 3:
            trennid_list2[num][1] = 'Kolmapaev'
        if i[1] == 4:
            trennid_list2[num][1] = 'Neljapaev'
        if i[1] == 5:
            trennid_list2[num][1] = 'Reede'
        if i[1] == 6:
            trennid_list2[num][1] = 'Laupaev'
        if i[1] == 7:
            trennid_list2[num][1] = 'Puhapaev'
        if i[1] == 7:
            trennid_list2[num][1] = 'Puhapaev'
        


    #print(trennid_list2)
    

    # for row in list(data_graafik):
    #     if row[1] == 1:
    #         #print(row)
    #         esmaspaev.append(row)
    #         esmaspaev_id.append(row[0])
    # ##print(esmaspaev[2])
    
    for row in list(data_v2ljak):
        # print("Id = ", row[0], )
        # print("Name = ", row[1])
        v2ljakud.append("{}".format(row[1]))
        #v2ljakud.append("{}".format(row[1]))
        #v2ljakud_id.append("{}".format(row[0]))
        #print(v2ljakud)

    for row in list(data_grupp):
        # print("Id = ", row[0], )
        # print("Name = ", row[1])
        #grupid.append(["{}","{}"].format(row[0],row[1]))
        grupid.append("{}".format(row[1]))
        grupid_id.append("{}".format(row[0]))
        print(grupid_id)
        #grupid_id.append("{}".format(row[0]))

   # minutidlist = []
    #cur = mysql.connection.cursor()
    #for i in grupid_id:
    #    vaikelist = []
    #   veelvaiksemlist = []        
    #    num = int(i)
    #    #print(type(num))
    #    #print(num)
    #    query_minutid = 'select t_minutes from graafik where grupp_id={}'.format(num)      
	#    #query_minutid = 'select t_minutes from graafik where grupp_id={}'.format(num)        
    #    cur.execute(query_minutid)
    #    data_minut = cur.fetchall()
    #    #print(data_minut)
    #    for j in data_minut:
    #        vaikelist.append(j)


     #   print(vaikelist)    
        #vaikelist.append(num)
        #vaikelist.append(data_minut)
        #minutidlist.append(vaikelist)
        
    #print(minutidlist)
	    #tyhilist.append(num,data_minut)
	    #uuslist.append(tyhilist)
    #print(uuslist)

    for row in list(data_treener):
        # print("Id = ", row[0], )
        # print("Name = ", row[1])
        #treenerid.append(["{}","{}"].format(row[0],row[1]))
        treenerid.append("{}".format(row[1]))
        #treenerid_id.append("{}".format(row[0]))
      
    if request.method == "POST":
        ## võta kasutaja sisestatud andmed
        details = request.form
        weekday = details['nadalapaev']
        treener = details['treenerid']
        v2ljak = details['v2ljakud']
        grupp = details['grupid']
        treeningtyyp = details['treeningtyyp']
        alguskell = details['alguskell']
        l6pukell = details['l6pukell']
    

        ## kuna kasutaja sisestab treeneri/grupi/väljaku nime, aga meil on vaja id
        ##siis võtame id nime järgi
        for row in data_treener:
            if treener == row[1]:
                treener_id = row[0]

        for row in data_v2ljak:
            if v2ljak == row[1]:
                v2ljak_id = row[0]

        for row in data_grupp:
            if grupp == row[1]:
                grupp_id = row[0]

        for row in el_nadalapaev:
            if weekday == row:
                weekday_id = el_nadalapaev.index(weekday)+1

        ##kontrollid
        ## alguskell on suurem kui lõpukell
        for row in el_aeg:
            if el_aeg.index(alguskell) >= el_aeg.index(l6pukell):
                #return 'kellaajad valed', 
                # flash('kellaajad valed')
                # return redirect(url_for('treening'))
                return redirect(url_for('viga1'))

        ## kas väljak on vaba
        for row in data_graafik:
            if weekday_id == row[1]:
                if v2ljak_id == row[4]:
                    ## kui samal ajal juba algab varasem treening VÕI  
                    ## alguskell on suurem kui  varasema treeningu algusaeg aga samal ajal ka väiksem kui varasema treeningu lõpuaeg
                    ## VÕI lõpukell on suurem kui varasema treeningu algusaeg
                    if alguskell == row[2] or (alguskell > row[2] and alguskell <= row[3]) or (alguskell < row[2] and l6pukell > row[2]):                         
                        return redirect(url_for('viga2'))
                        #flash('Sellel ajal on juba treening')
                        #return redirect(url_for('treening'))
        
        
        #### Treeneril võib olla samal ajal olla mitmel väljakul treening
        # for row in data_graafik:
        #     if weekday_id == row[1]:
        #         if treener_id == row[6]:
        #             if alguskell == row[2] or (alguskell > row[2] and alguskell <= row[3]) or (alguskell < row[2] and l6pukell > row[2]):
        #                 return "Treeneril on juba samal ajal treening"
        
        for row in data_graafik:
            if weekday_id == row[1]:
                if grupp_id == row[5]:
                    if alguskell == row[2] or (alguskell > row[2] and alguskell <= row[3]) or (alguskell < row[2] and l6pukell > row[2]):
                        return redirect(url_for('viga3'))
                        #return "Grupil on samal ajal juba trenn"
                        #flash('Grupil on samal ajal juba trenn')
                        #return redirect(url_for('treening'))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO graafik(weekday,start_time,end_time,valjak_id,grupp_id,treener_id,t_type,hooaeg_id ) VALUES ('{}','{}','{}','{}','{}','{}','{}',{})".format(weekday_id,alguskell,l6pukell,v2ljak_id,grupp_id,treener_id,treeningtyyp,hooaeg_praegu))
  
        mysql.connection.commit()
        cur.close()




        
        return redirect(url_for('graafik'))



    ##dropdown_list = ['Maali Maasikas', 'Peeter Kaalikas', 'Jaak Peet']
    # if request.method == "POST":
    #     select = request.form.get('treenerid')
    #return(str(select)) # just to see what select is
    
    return render_template('treening.html',trennid_list2=trennid_list2, trennid=trennid,v2ljakud=v2ljakud,grupid=grupid,treenerid=treenerid,el_weekdays=el_weekdays,el_aeg=el_aeg,el_nadalapaev=el_nadalapaev,treeningtyyp=treeningtyyp)

@app.route('/tasemed', methods=['GET', 'POST'])
def tasemed():
    
    query_tase = 'select * from tase'
    cur = mysql.connection.cursor()
    cur.execute(query_tase)
    pealkirjad = cur.description
    data_tase = cur.fetchall()
    cur.close()

    tase_list = [list(row) for row in data_tase] # list of lists
    
    for num, i in enumerate(tase_list):
        if i[6] == 0:
            tase_list[num][6] = 'Mitteaktiivne'
        if i[6] == 1:
            tase_list[num][6] = 'Aktiivne'
    print(tase_list)

    if request.method == "POST":
        details = request.form
        nimi = details['nimi']
        tyyp1 = details['tyyp1']
        tunnid1 = details['tunnid1']
        tyyp2 = details['tyyp2']
        tunnid2 = details['tunnid2']
        staatus = 1

        cur = mysql.connection.cursor()
        print(nimi)


        cur.execute("INSERT INTO tase(name,type1,hours1,type2,hours2,status) VALUES ('{}', '{}','{}', '{}','{}','{}')".format(nimi,tyyp1,tunnid1,tyyp2,tunnid2,staatus))

        mysql.connection.commit()
        cur.close()
        return redirect('/tasemed')


    return render_template('tasemed.html', pealkirjad=pealkirjad,data_tase=data_tase,tase_list=tase_list)

@app.route('/hooaeg', methods=['GET', 'POST'])
def hooaeg():
    


    return render_template('hooaeg.html')

@app.route('/treeningsaalid', methods=['GET', 'POST'])
def treeningsaalid():
    
    query_valjak = 'select * from valjak'
    cur = mysql.connection.cursor()
    cur.execute(query_valjak)
    pealkirjad = cur.description
    data_valjak = cur.fetchall()
    cur.close()

    valjak_list = [list(row) for row in data_valjak] # list of lists
    
    for num, i in enumerate(valjak_list):
        if i[2] == 0:
            valjak_list[num][2] = 'Mitteaktiivne'
        if i[2] == 1:
            valjak_list[num][2] = 'Aktiivne'
    print(valjak_list)

    if request.method == "POST":
        details = request.form
        nimi = details['nimi']
        status = 1

        cur = mysql.connection.cursor()
        print(nimi)


        cur.execute("INSERT INTO valjak(name,status) VALUES ('{}', '{}')".format(nimi,status))

        mysql.connection.commit()
        cur.close()
        return redirect('/treeningsaalid')


    return render_template('treeningsaalid.html', pealkirjad=pealkirjad,data_valjak=data_valjak,valjak_list=valjak_list)

@app.route('/grupid', methods=['GET'])
def grupid():
    
    cur = mysql.connection.cursor()

    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()    
    hooaeg_praegu = hooaeg_max[0][0]

    query_grupp = 'select * from grupp where hooaeg_id={}'.format(hooaeg_praegu)
    cur.execute(query_grupp)
    data_grupp = cur.fetchall() 
    
    opilased_grupp_list = []
    for i in data_grupp:
        v2ike_list = []
        query_opilased_grupp = 'select opilane.name from grupp_opilane inner join opilane on grupp_opilane.opilane_id=opilane.id where hooaeg_id={} and grupp_id={}'.format(hooaeg_praegu,i[0]) 
        cur.execute(query_opilased_grupp)
        data_opilas_grupp = cur.fetchall()
        v2ike_list.append(i[1])

        vga_v2ike_list = []
        for l in data_opilas_grupp:
            for f in l:
                vga_v2ike_list.append(f)

        #v2ike_list.append(data_opilas_grupp)
        v2ike_list.append(vga_v2ike_list)
        opilased_grupp_list.append(v2ike_list)

    # print(opilased_grupp_list)

    cur.close()
    return render_template('grupid.html',opilased_grupp_list=opilased_grupp_list)


@app.route('/opilased', methods=['GET', 'POST'])
def opilased():
    
    query_opilased = 'select * from opilane'
    cur = mysql.connection.cursor()
    cur.execute(query_opilased)
    pealkirjad = cur.description
    data_opilased = cur.fetchall()
    cur.close()

    opilased_list = [list(row) for row in data_opilased] # list of lists
    
    for num, i in enumerate(opilased_list):
        if i[6] == 0:
            opilased_list[num][6] = 'Mitteaktiivne'
        if i[6] == 1:
            opilased_list[num][6] = 'Aktiivne'
    print(opilased_list)

    if request.method == "POST":
        details = request.form
        nimi = details['nimi']
        aadress = details['aadress']
        regioon = details['regioon']
        telefon = details['telefon']
        email = details['email']
        status = 1

        cur = mysql.connection.cursor()
        print(nimi)


        cur.execute("INSERT INTO opilane(name,address,region,phone,email,status) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(nimi,aadress,regioon,telefon,email,status))

        mysql.connection.commit()
        cur.close()
        return redirect('/opilased')


    return render_template('opilased.html', pealkirjad=pealkirjad,data_opilased=data_opilased,opilased_list=opilased_list)  

@app.route('/treenerid', methods=['GET', 'POST'])
def treenerid():
    
    query_treener = 'select * from treener'
    cur = mysql.connection.cursor()
    cur.execute(query_treener)
    pealkirjad = cur.description
    data_treener = cur.fetchall()
    cur.close()

    treener_list = [list(row) for row in data_treener] # list of lists

    for num, i in enumerate(treener_list):
        if i[4] == 0:
            treener_list[num][4] = 'Mitteaktiivne'
        if i[4] == 1:
            treener_list[num][4] = 'Aktiivne'
    

    if request.method == "POST":
        details = request.form
        nimi = details['nimi']
        telefon = details['telefon']
        email = details['email']
        status = 1

        cur = mysql.connection.cursor()
        print(nimi)


        cur.execute("INSERT INTO treener(name,phone,email,status) VALUES ('{}', '{}', '{}', '{}')".format(nimi,telefon,email,status))

        mysql.connection.commit()
        cur.close()
        return redirect('/treenerid')


    return render_template('treenerid.html', treener_list=treener_list)  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()


        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES ('{}', '{}')".format(firstName, lastName))

        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


@app.route('/hooajad', methods=['GET', 'POST'])
def hooajad():

    if request.method == "POST":
        details = request.form
        nimi = details['nimi']
        
        cur = mysql.connection.cursor()
        print(nimi)

        cur.execute("INSERT INTO hooaeg (name) VALUES ('{}')".format(nimi))

        mysql.connection.commit()
        cur.close()
        return redirect('/hooaeglisatud')
        
    return render_template('hooajad.html')


@app.route('/hooaeglisatud', methods=['GET'])
def hooaeglisatud():

    return render_template('hooaeglisatud.html')

@app.route('/graafik', methods=['GET'])
def graafik():
    p2eva_lingid = '<a href="paev7">&larr;Eelmine</a> &nbsp; <b style="font-size:22px">Esmaspäev</b> &nbsp; <a href="paev2">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 1".format(hooaeg_praegu)    

    query_v2ljak = 'select * from valjak where status=1;'
    
    cur.execute(query_v2ljak)
    data_v2ljak = cur.fetchall() 

    cur.execute(guery_gr_join)
    data_gr_join = cur.fetchall()    

    cur.close()

    v2ljakud = []    
    v2ljakud_id = []
    for row in list(data_v2ljak):
        v2ljakud.append("{}".format(row[1]))
        v2ljakud_id.append(row[0])
    
    #print(v2ljakud)
    #print(v2ljakud_id)
    #print('data graafik join',data_gr_join)
  
    v2ljakud_id_preagu = []
    for row in data_gr_join:
        #print("Id = ", row[0])
        #print("weekday = ", row[1])
        #print("start_time = ", row[2])
        #print("end_time = ", row[3])
        #print("valjak = ", row[4])
        #print("valjak_id = ", row[5])
        #print("grupp_id = ", row[6])
        #print("treener_id = ", row[7])
        #print("treening_tyyp = ", row[8])
        v2ljakud_id_preagu.append(row[5])
    print("id preegu",v2ljakud_id_preagu)


    # loome v2ljak_id_atm ja sisestame sinna väljakute j2jekorra, selleks et n2iteks kui v2ljak 2 ja 3 on pandud inactive olekusse
    # siis t2nu sellele oleks ka j2jrekorra numbrid v2iksemad, ja nr6 v2ljak ei oleks j2jrekorras ja tabelis nr6
    v2ljak_id_atm = []
    for f in v2ljakud_id_preagu:
        for num33, g in enumerate(v2ljakud_id):
            if f == g:
                v2ljak_id_atm.append(num33+1)


    # teeme tuple ymberkorralikuks listiks
          
    # print(data_graafik)
    el_weekdays_list = []
    pop_inf_list = []
    # print(el_weekdays)
    
    # tekitame listi, kus sees mitu listi, ning iga v2ikse listi esimene element, on kella-aeg
    # PS! antud listid l2hevad graafiku t2iteks
    for num1, i in enumerate(el_weekdays):
        sml_lst = []
        # sml_lst.append(i)
        sml_lst.append("<td>{}</td>".format(i))

        
        kella_aeg = i.split(" - ")[0]
        
        # algul t2idame k6ik tabeli read by default tyhikutega, ning hiljem vahetame vajalikud tyhiku kohad v2lja t2htsa infoga
        for m in range(0,len(v2ljakud)):
            # sml_lst.append(" ")
            sml_lst.append("<td> </td>")

        # m on tuplete kogumik, kogu graafik databaasi tabelist, ning j2rgnevalt vaadakse, kas kas kellaeg klapib m6ne sissekandega
        for num44, m in enumerate(data_gr_join):
            if kella_aeg in m[2]:

                # print(m[2])   # <-- trenni algus aeg
                # print(m[3])   # <-- trenni l6pp aeg 

                # teada saamaks, kuna treening l6ppeb; ehk otisme v2lja kuna el_weekdays listis
                # trenni l6ppmisaeg on m6ne muu trenni algusaeg
                tr_wh = 0
                while True:
                    if m[3] == el_weekdays[num1+tr_wh].split(" - ")[0]:
                        break
                    tr_wh = tr_wh + 1
                    if tr_wh > 50:
                        break
                    
                    
                # print(el_weekdays[num1], el_weekdays[num1+tr_wh].split(" - ")[0], tr_wh)                
                    
                
                # kui treening on pikem kui 1 graafiku row-cell, pikendatakse vastava row cell:
                if tr_wh >= 2:
                    #sml_lst[m[5]] = '<td rowspan="{}">{} | {} - {}</td>'.format(tr_wh,m[6],m[7],m[8])                    
                    sml_lst[v2ljak_id_atm[num44]] = '<td rowspan="{}">{} | {} - {}</td>'.format(tr_wh,m[6],m[7],m[8])                        
                                        
                    # pop_inf listi lisatakse info, mida tuleks p2rast poppida, et graafik oleks silmale ilus.                    
                    pop_inf_list.append([num1,v2ljak_id_atm[num44],tr_wh])
                                    
                else:
                    #sml_lst[m[5]] = "<td>{} | {} - {}</td>".format(m[6],m[7],m[8])
                    sml_lst[v2ljak_id_atm[num44]] = "<td>{} | {} - {}</td>".format(m[6],m[7],m[8])

                    
        el_weekdays_list.append(sml_lst)
        
   
    # yritame el_weekdays_list -ist v2lja poppida soovimatud elemendid, kasutades selleks infot, mis on pop_inf_list -is.
    # poppine k2ib listi m6ttes alt yles, mitte ylalt alla, sestap kasutatateks reversed(list) funktsiooni
    # lambda funktsiooni eksm2rk on, et sorted list sort-itaske koigepealt i[0] kohapealt ja siis peale seda i[1]
    pop_inf_list_fix = sorted(pop_inf_list, key=lambda x: (int(x[0]), x[1]))
    for i in reversed(pop_inf_list_fix):
        for m in range(0,i[2]-1):
            el_weekdays_list[i[0]+1+m].pop(i[1])
    

    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)


paev_treeningplaan ='''
query_v2ljak = 'select * from valjak where status=1;'
    
cur.execute(query_v2ljak)
data_v2ljak = cur.fetchall() 

cur.execute(guery_gr_join)
data_gr_join = cur.fetchall()    

cur.close()

v2ljakud = []    
v2ljakud_id = []
for row in list(data_v2ljak):
    v2ljakud.append("{}".format(row[1]))
    v2ljakud_id.append(row[0])
    
#print(v2ljakud)
#print(v2ljakud_id)
#print('data graafik join',data_gr_join)
  
v2ljakud_id_preagu = []
for row in data_gr_join:
    #print("Id = ", row[0])
    #print("weekday = ", row[1])
    #print("start_time = ", row[2])
    #print("end_time = ", row[3])
    #print("valjak = ", row[4])
    #print("valjak_id = ", row[5])
    #print("grupp_id = ", row[6])
    #print("treener_id = ", row[7])
    #print("treening_tyyp = ", row[8])
    v2ljakud_id_preagu.append(row[5])
print("id preegu",v2ljakud_id_preagu)


# loome v2ljak_id_atm ja sisestame sinna väljakute j2jekorra, selleks et n2iteks kui v2ljak 2 ja 3 on pandud inactive olekusse
# siis t2nu sellele oleks ka j2jrekorra numbrid v2iksemad, ja nr6 v2ljak ei oleks j2jrekorras ja tabelis nr6
v2ljak_id_atm = []
for f in v2ljakud_id_preagu:
    for num33, g in enumerate(v2ljakud_id):
        if f == g:
            v2ljak_id_atm.append(num33+1)


# teeme tuple ymberkorralikuks listiks
          
# print(data_graafik)
el_weekdays_list = []
pop_inf_list = []
# print(el_weekdays)
    
# tekitame listi, kus sees mitu listi, ning iga v2ikse listi esimene element, on kella-aeg
# PS! antud listid l2hevad graafiku t2iteks
for num1, i in enumerate(el_weekdays):
    sml_lst = []
    # sml_lst.append(i)
    sml_lst.append("<td>{}</td>".format(i))

        
    kella_aeg = i.split(" - ")[0]
        
    # algul t2idame k6ik tabeli read by default tyhikutega, ning hiljem vahetame vajalikud tyhiku kohad v2lja t2htsa infoga
    for m in range(0,len(v2ljakud)):
        # sml_lst.append(" ")
        sml_lst.append("<td> </td>")

    # m on tuplete kogumik, kogu graafik databaasi tabelist, ning j2rgnevalt vaadakse, kas kas kellaeg klapib m6ne sissekandega
    for num44, m in enumerate(data_gr_join):
        if kella_aeg in m[2]:

            # print(m[2])   # <-- trenni algus aeg
            # print(m[3])   # <-- trenni l6pp aeg 

            # teada saamaks, kuna treening l6ppeb; ehk otisme v2lja kuna el_weekdays listis
            # trenni l6ppmisaeg on m6ne muu trenni algusaeg
            tr_wh = 0
            while True:
                if m[3] == el_weekdays[num1+tr_wh].split(" - ")[0]:
                    break
                tr_wh = tr_wh + 1
                if tr_wh > 50:
                    break
                    
                    
            # print(el_weekdays[num1], el_weekdays[num1+tr_wh].split(" - ")[0], tr_wh)                
                    
                
            # kui treening on pikem kui 1 graafiku row-cell, pikendatakse vastava row cell:
            if tr_wh >= 2:
                #sml_lst[m[5]] = '<td rowspan="{}">{} | {} - {}</td>'.format(tr_wh,m[6],m[7],m[8])                    
                sml_lst[v2ljak_id_atm[num44]] = '<td rowspan="{}">{} | {} - {}</td>'.format(tr_wh,m[6],m[7],m[8])                        
                                        
                # pop_inf listi lisatakse info, mida tuleks p2rast poppida, et graafik oleks silmale ilus.                    
                pop_inf_list.append([num1,v2ljak_id_atm[num44],tr_wh])
                                    
            else:
                #sml_lst[m[5]] = "<td>{} | {} - {}</td>".format(m[6],m[7],m[8])
                sml_lst[v2ljak_id_atm[num44]] = "<td>{} | {} - {}</td>".format(m[6],m[7],m[8])

                    
    el_weekdays_list.append(sml_lst)
        
   
# yritame el_weekdays_list -ist v2lja poppida soovimatud elemendid, kasutades selleks infot, mis on pop_inf_list -is.
# poppine k2ib listi m6ttes alt yles, mitte ylalt alla, sestap kasutatateks reversed(list) funktsiooni
# lambda funktsiooni eksm2rk on, et sorted list sort-itaske koigepealt i[0] kohapealt ja siis peale seda i[1]
pop_inf_list_fix = sorted(pop_inf_list, key=lambda x: (int(x[0]), x[1]))
for i in reversed(pop_inf_list_fix):
    for m in range(0,i[2]-1):
        el_weekdays_list[i[0]+1+m].pop(i[1])'''



@app.route('/paev1', methods=['GET'])
def paev1():
    p2eva_lingid = '<a href="paev7">&larr;Eelmine</a> &nbsp; <b style="font-size:20px">Esmaspäev</b> &nbsp; <a href="paev2">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 1".format(hooaeg_praegu)    
    exec(paev_treeningplaan)
    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)

@app.route('/paev2', methods=['GET'])
def paev2():
    p2eva_lingid = '<a href="paev1">&larr;Eelmine</a> &nbsp; <b style="font-size:20px">Teisipäev</b> &nbsp; <a href="paev3">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 2".format(hooaeg_praegu)    
    exec(paev_treeningplaan)
    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)

@app.route('/paev3', methods=['GET'])
def paev3():
    p2eva_lingid = '<a href="paev2">&larr;Eelmine</a> &nbsp; <b style="font-size:20px">Kolmapäev</b> &nbsp; <a href="paev4">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 3".format(hooaeg_praegu)    
    exec(paev_treeningplaan)
    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)

@app.route('/paev4', methods=['GET'])
def paev4():
    p2eva_lingid = '<a href="paev3">&larr;Eelmine</a> &nbsp; <b style="font-size:20px">Neljapäev</b> &nbsp; <a href="paev5">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 4".format(hooaeg_praegu)    
    exec(paev_treeningplaan)
    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)

@app.route('/paev5', methods=['GET'])
def paev5():
    p2eva_lingid = '<a href="paev4">&larr;Eelmine</a> &nbsp; <b style="font-size:20px">Reede</b> &nbsp; <a href="paev6">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 5".format(hooaeg_praegu)    
    exec(paev_treeningplaan)
    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)

@app.route('/paev6', methods=['GET'])
def paev6():
    p2eva_lingid = '<a href="paev5">&larr;Eelmine</a> &nbsp; <b style="font-size:20px">Laupäev</b> &nbsp; <a href="paev7">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 6".format(hooaeg_praegu)    
    exec(paev_treeningplaan)
    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)

@app.route('/paev7', methods=['GET'])
def paev7():
    p2eva_lingid = '<a href="paev6">&larr;Eelmine</a> &nbsp; <b style="font-size:20px">Pühapäev</b> &nbsp; <a href="paev1">Järgmine&rarr;</a>'
    cur = mysql.connection.cursor()
    cur.execute('select max(id) from hooaeg')
    hooaeg_max = cur.fetchall()
    hooaeg_praegu = hooaeg_max[0][0]    
    guery_gr_join = "select graafik.id, graafik.weekday, graafik.start_time, graafik.end_time, valjak.name as valjakname, graafik.valjak_id, grupp.name as gruppname, treener.name as treenername, graafik.t_type, graafik.t_minutes from graafik inner join valjak on graafik.valjak_id=valjak.id inner join grupp on graafik.grupp_id=grupp.id inner join treener on graafik.treener_id=treener.id where graafik.hooaeg_id = {} and graafik.weekday = 7".format(hooaeg_praegu)    
    exec(paev_treeningplaan)
    return render_template('graafik.html', v2ljakud=v2ljakud,el_weekdays_list=el_weekdays_list,p2eva_lingid=p2eva_lingid)

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/basecopy')
def basecopy():
    return render_template('basecopy.html')

if __name__ == '__main__':
    app.run()
#



# kui oli issue flask-mysqldb moodulit installida mari serverile, aitas:
# apt-get install -y python-setuptools
# apt-get install libmysqlclient-dev
# apt-get install build-essential libssl-dev libffi-dev python-dev
# pip install --user flask-mysqldb  # <-- not sure kas sellest oli miskit tolku
# pip install flask-mysqldb



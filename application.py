from flask import Flask, render_template,request, session
import pandas as pd
import pulp
import os

app = Flask(__name__)
app.secret_key = 'dietproblem'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/BREAKFAST', methods=['POST'])
def bmi_calc():
    if request.method == 'POST':
        ht = float(request.form.get("height"))
        wt = float(request.form.get("weight"))
        #print(ht,wt)
        bmi = (wt / (ht ** 2.0)) * 730.0
        #print(bmi)
        age = int(request.form.get("age"))
        work = request.form.get("work")
        gender = request.form.get("gender")
        print(age,work,gender)
        df1 = pd.read_csv("C:\\Users\Aakanksha\\Documents\\MS CPE\\Spring 2018\\DietProblem_Solver\\male_age_calorie.csv")
        df2 = pd.read_csv("C:\\Users\Aakanksha\\Documents\\MS CPE\\Spring 2018\\DietProblem_Solver\\female_age_calorie.csv")
        if (bmi >= 17 and bmi <= 24.9):
            if (gender == 'Female'):
                if (age > 76):
                    min_cal = df2.loc[74, work.upper()]
                else:
                    min_cal = df2.loc[int(age) - 2, work.upper()]
            else:
                if (age > 76):
                    min_cal = df1.loc[74, work.upper()]
                else:
                    min_cal = df1.loc[int(age) - 2, work.upper()]
            msg = "Great! Your BMI is normal and you are healthy. Keep maintaining the weight an live a happy and healthy life!"
        elif(bmi<=16.9):
            if (gender == 'Female'):
                if (age > 76):
                    min_cal = df2.loc[74, work.upper()]
                else:
                    min_cal = df2.loc[int(age) - 2, work.upper()]
            else:
                if (age > 76):
                    min_cal = df1.loc[74, work.upper()]
                else:
                    min_cal = df1.loc[int(age) - 2, work.upper()]
            msg = "Attention! Your BMI is low. You must intake more calorie and work on increasing your weight for a healthy life!"
        elif(bmi>=25):
            if (gender == 'Female'):
                if (age > 76):
                    min_cal = df2.loc[74, work.upper()]
                else:
                    min_cal = df2.loc[int(age) - 2, work.upper()]
            else:
                if (age > 76):
                    min_cal = df1.loc[74, work.upper()]
                else:
                    min_cal = df1.loc[int(age) - 2, work.upper()]
            msg = "Attention! Your BMI is very high. You must intake required calories and focus on workout to decrease your weight for a healthy life!"
        session['min_cal'] = int(min_cal)
        session['wt'] = float(wt)
        return render_template('break.html', bmi = str(round(bmi,2)), msg = msg, min_cal = min_cal)

@app.route('/LUNCH', methods=['POST','GET'])
def bf():
    #min_cal = 2400
    if(request.method == 'POST'):
        min_cal = int(session.get('min_cal', None))
        wt = float(session.get('wt', None))
        print(min_cal)
        lpp = pulp.LpProblem("My LP Problem", pulp.LpMinimize)
        x = pulp.LpVariable('x', lowBound=0, cat='Continuous') #Fruit 1
        y = pulp.LpVariable('y', lowBound=0, cat='Continuous') #Fruit 2
        z = pulp.LpVariable('z', lowBound=0, cat='Continuous') #Fruit 3
        a = pulp.LpVariable('a', lowBound=0, cat='Continuous') #Fruit 4
        b = pulp.LpVariable('b', lowBound=0, cat='Continuous') #Bread
        t = pulp.LpVariable('t', lowBound=0, cat='Continuous') #Beverage
        u = pulp.LpVariable('u', lowBound=0, cat='Continuous') #Meat
        v = pulp.LpVariable('v', lowBound=0, cat='Continuous') #Eggs
        w = pulp.LpVariable('w', lowBound=0, cat='Continuous') #Oats
        calorie = []
        fat = []
        carbs = []
        proteins = []
        cost = []
        df3 = pd.read_csv("C:\\Users\Aakanksha\\Documents\\MS CPE\\Spring 2018\\DietProblem_Solver\\NutritionalFacts.csv", encoding="utf8")
        df4 = df3.set_index("Food and Serving", drop= False)
        var_cnt = 0
        fruits = request.form.getlist("fruit_list")
        var_cnt=len(fruits)
        print(var_cnt)
        for i in range(0,len(fruits)):
            cal = df4.loc[fruits[i],"Calories"]
            price = df4.loc[fruits[i],"Cost"]
            carb = df4.loc[fruits[i],"Carbohydrate"]
            fats = df4.loc[fruits[i],"Total Fat"]
            prt = df4.loc[fruits[i],"Protein"]
            print(cal)
            calorie.append(cal)
            cost.append(price)
            carbs.append(carb)
            fat.append(fats)
            proteins.append(prt)
        for j in range(0,4-len(fruits)):
            calorie.append(0)
            cost.append(0)
            carbs.append(0)
            fat.append(0)
            proteins.append(0)
        bread = request.form.get("bread")
        cal_bread = df4.loc[bread,"Calories"]
        #calorie.append(cal_bread)
        price_bread = df4.loc[bread, "Cost"]
        #cost.append(price_bread)
        carb_bread = df4.loc[bread, "Carbohydrate"]
        prt_bread = df4.loc[bread, "Protein"]
        fat_bread = df4.loc[bread, "Total Fat"]
        beverage = request.form.get("beverage")
        cal_bev = df4.loc[beverage, "Calories"]
        #calorie.append(cal_bev)
        price_bev = df4.loc[beverage, "Cost"]
        #cost.append(price_bev)
        carb_bev = df4.loc[beverage,"Carbohydrate"]
        prt_bev = df4.loc[beverage,"Protein"]
        fat_bev = df4.loc[beverage,"Total Fat"]
        var_cnt += 2
        print(var_cnt)
        meat = request.form.get("meat")
        if(meat!="None"):
            var_cnt+=1
            cal_meat = df4.loc[meat,"Calories"]
            #calorie.append(cal_meat)
            price_meat = df4.loc[meat, "Cost"]
            #cost.append(price_meat)
            carb_meat = df4.loc[meat, "Carbohydrate"]
            prt_meat = df4.loc[meat, "Protein"]
            fat_meat = df4.loc[meat, "Total Fat"]
        else:
            cal_meat = 0
            price_meat = 0
            carb_meat = 0
            prt_meat = 0
            fat_meat = 0
        eggs = request.form["eggs"]
        print(eggs)
        if(eggs=='Yes'):
            var_cnt+=1
            cal_eggs = df4.loc["Egg (2 egg/serving)","Calories"]
            #calorie.append(cal_eggs)
            price_egg = df4.loc["Egg (2 egg/serving)", "Cost"]
            #cost.append(price_egg)
            carb_egg = df4.loc["Egg (2 egg/serving)", "Carbohydrate"]
            prt_egg = df4.loc["Egg (2 egg/serving)", "Protein"]
            fat_egg = df4.loc["Egg (2 egg/serving)", "Total Fat"]
        else:
            cal_eggs = 0
            price_egg = 0
            carb_egg = 0
            prt_egg = 0
            fat_egg = 0
        # oats = request.form["oats"]
        # if(oats=='Yes'):
        #     var_cnt+=1
        #     cal_oats = df4.loc["Oats","Calories"]
        #     #calorie.append(cal_oats)
        #     price_oats = df4.loc["Oats","Cost"]
        #     #cost.append(price_oats)
        #     carb_oats = df4.loc["Oats","Carbohydrate"]
        #     prt_oats = df4.loc["Oats","Protein"]
        #     fat_oats = df4.loc["Oats","Total Fat"]
        # else:
        #     cal_oats = 0
        #     price_oats = 0
        #     carb_oats = 0
        #     prt_oats = 0
        #     fat_oats = 0
        print(fruits,bread,beverage,meat,eggs,var_cnt)
        Total_prt = 0.37 * wt
        print(calorie)

        # Objective function
        lpp += cost[0] * x + cost[1] * y + price_bread*b + price_bev*t + price_meat*u + price_egg*v, "Z"

        Total_cal_bf = 0.2*min_cal

        # contraints
        lpp += carbs[0] * x + carbs[1]*y >= 15 #carb
        lpp += carb_bread * b + carb_bev * t >= 25  # carb
        lpp += carbs[0] * x + carbs[1] * y  <= 35  # carb
        lpp += carb_bread * b + carb_bev * t <= 60  # carb
        lpp += proteins[0] * x + proteins[1]*y+ prt_bread * b + prt_bev * t + prt_meat * u + prt_egg * v >= Total_prt/4 #protein
        lpp += fat[0] *x + fat[1] *y + fat[2]*z + fat[3] * a + fat_bread * b + fat_bev * t + fat_meat * u + fat_egg * v >= 11 #fats
        lpp += fat[0] * x + fat[1] * y + fat[2] * z + fat[3] * a + fat_bread * b + fat_bev * t + fat_meat * u + fat_egg * v <= 20  # fats
        lpp += calorie[0] * x + calorie[1]*y +calorie[2]*z + calorie[3] * a + cal_bread*b + cal_bev*t + cal_meat*u + cal_eggs *v >= Total_cal_bf # Calories
        lpp += x + y + z + a >= 0.5
        lpp += x + y + z + a <= 4
        lpp.solve()
        ans = pulp.LpStatus[lpp.status]
        print(ans)
        bf_qty = {}
        for variable in lpp.variables():
            print("{} = {}".format(variable.name, variable.varValue))
            if(variable.name == 'x'):
                bf_qty[fruits[0]] = variable.varValue
            elif(variable.name == 'y'):
                bf_qty[fruits[1]] = variable.varValue
            elif (variable.name == 'z'):
                bf_qty[fruits[2]] = variable.varValue
            elif (variable.name == 'a'):
                bf_qty[fruits[3]] = variable.varValue
            elif (variable.name == 'b'):
                bf_qty[bread] = variable.varValue
            elif (variable.name == 't'):
                bf_qty[beverage] = variable.varValue
            elif (variable.name == 'u' and meat!='None'):
                bf_qty[meat] = variable.varValue
            elif(variable.name == 'v' and eggs=='Yes'):
                bf_qty['Eggs'] = variable.varValue
            #bf_qty[variable.name] = variable.varValue

        print(pulp.value(lpp.objective))
        cst = pulp.value(lpp.objective)
        print(bf_qty)
        print(cst)
        session['bfcost'] = cst
        session['bf_val'] = bf_qty
        return render_template('lunch.html')

@app.route('/SNACK', methods=['POST','GET'])
def lunch():
    if(request.method == 'POST'):
        i =0
        j = 0
        k = 0
        l = 0
        wt = float(session.get('wt', None))
        min_cal = int(session.get('min_cal', None))
        Total_prt = 0.37 * wt

        lpp_l = pulp.LpProblem("My LP Problem", pulp.LpMinimize)
        br = pulp.LpVariable('br', lowBound=0, cat='Continuous')  # carb essential
        ms = pulp.LpVariable('ms', lowBound=0, cat='Continuous')  # meat and sea food
        v1 = pulp.LpVariable('v1', lowBound=0, cat='Continuous')  # veggie 1
        v2 = pulp.LpVariable('v2', lowBound=0, cat='Continuous')  # veggie 2
        v3 = pulp.LpVariable('v3', lowBound=0, cat='Continuous')  # veggie 3
        v4 = pulp.LpVariable('v4', lowBound=0, cat='Continuous')  # veggie 4
        g1 = pulp.LpVariable('g1', lowBound=0, cat='Continuous')  # green 1
        g2 = pulp.LpVariable('g2', lowBound=0, cat='Continuous')  # green 2
        g3 = pulp.LpVariable('g3', lowBound=0, cat='Continuous')  # green 3
        #g4 = pulp.LpVariable('g4', lowBound=0, cat='Continuous')  # green 4
        c = pulp.LpVariable('c', lowBound=0, cat='Continuous')  # cheese
        cost_v = []
        calorie_v = []
        fat_v = []
        carbs_v = []
        proteins_v = []
        cost_g = []
        calorie_g = []
        fat_g = []
        carbs_g = []
        proteins_g = []
        df3 = pd.read_csv("C:\\Users\Aakanksha\\Documents\\MS CPE\\Spring 2018\\DietProblem_Solver\\NutritionalFacts.csv",encoding="utf8")
        df4 = df3.set_index("Food and Serving", drop=False)
        ess_carbs = request.form.get("carb_list")
        ms_list = request.form.get("ms_list")
        veg_list = request.form.getlist("veggie_list")
        green_list = request.form.getlist("green_list")
        chesse_type = request.form.get("cheese_list")

        cal_ec = df4.loc[ess_carbs,"Calories"]
        price_ec = df4.loc[ess_carbs,"Cost"]
        carb_ec = df4.loc[ess_carbs,"Carbohydrate"]
        fats_ec = df4.loc[ess_carbs,"Total Fat"]
        prt_ec = df4.loc[ess_carbs,"Protein"]
        print(cal_ec)
        for i in range(0,len(veg_list)):
            cal_v = df4.loc[veg_list[i],"Calories"]
            price_v = df4.loc[veg_list[i],"Cost"]
            carb_v = df4.loc[veg_list[i],"Carbohydrate"]
            fats_v = df4.loc[veg_list[i],"Total Fat"]
            prt_v = df4.loc[veg_list[i],"Protein"]
            print(cal_v)
            calorie_v.append(cal_v)
            cost_v.append(price_v)
            carbs_v.append(carb_v)
            fat_v.append(fats_v)
            proteins_v.append(prt_v)
        for j in range(0,4-len(veg_list)):
            calorie_v.append(0)
            cost_v.append(0)
            carbs_v.append(0)
            fat_v.append(0)
            proteins_v.append(0)
        for k in range(0,len(green_list)):
            cal_g = df4.loc[green_list[k],"Calories"]
            price_g = df4.loc[green_list[k],"Cost"]
            carb_g = df4.loc[green_list[k],"Carbohydrate"]
            fats_g = df4.loc[green_list[k],"Total Fat"]
            prt_g = df4.loc[green_list[k],"Protein"]
            print(cal_g)
            calorie_g.append(cal_g)
            cost_g.append(price_g)
            carbs_g.append(carb_g)
            fat_g.append(fats_g)
            proteins_g.append(prt_g)
        for l in range(0,3-len(green_list)):
            calorie_g.append(0)
            cost_g.append(0)
            carbs_g.append(0)
            fat_g.append(0)
            proteins_g.append(0)
        if(ms_list == 'None'):
            ms_cal = 0
            price_ms = 0
            carb_ms = 0
            prt_ms = 0
            fat_ms = 0

        else:
            ms_cal = df4.loc[ms_list, "Calories"]
            # calorie.append(cal_bread)
            price_ms = df4.loc[ms_list, "Cost"]
            # cost.append(price_ms)
            carb_ms = df4.loc[ms_list, "Carbohydrate"]
            prt_ms = df4.loc[ms_list, "Protein"]
            fat_ms = df4.loc[ms_list, "Total Fat"]

        if(chesse_type == 'None'):
            ch_cal = 0
            price_ch = 0
            carb_ch = 0
            prt_ch = 0
            fat_ch = 0
        else:
            ch_cal = df4.loc[chesse_type, "Calories"]
            # calorie.append(cal_bread)
            price_ch = df4.loc[chesse_type, "Cost"]
            # cost.append(price_ms)
            carb_ch = df4.loc[chesse_type, "Carbohydrate"]
            prt_ch = df4.loc[chesse_type, "Protein"]
            fat_ch = df4.loc[chesse_type, "Total Fat"]
        print(len(green_list), len(veg_list))
        # Objective function
        lpp_l += price_ms *ms + price_ec * br + cost_v[0] * v1 + cost_g[0] * g1 + cost_v[1] * v2 + cost_g[1] * g2 + cost_v[2] * v3 + cost_g[2] * g3 + cost_v[3] * v4 + price_ch * c, "Z"

        Total_cal_l = 0.3 * min_cal

        # contraints
        lpp_l += carb_ms*ms + carb_ec * br + carb_ch * c >= 15  # carb
        lpp_l += carbs_v[0] * v1 + carbs_g[0] * g1 + carbs_v[1] * v2 + carbs_g[1] * g2 + carbs_v[2] * v3 + carbs_g[2] * g3 + carbs_v[3] * v4 >=15
        lpp_l += carb_ms * ms + carb_ec * br + carb_ch * c <= 40  # carb
        lpp_l += carbs_v[0] * v1 + carbs_g[0] * g1 + carbs_v[1] * v2 + carbs_g[1] * g2 + carbs_v[2] * v3 + carbs_g[2] * g3 + carbs_v[3] * v4>= 30
        lpp_l += prt_ms *ms + prt_ec * br + proteins_v[0] * v1 + proteins_g[0] * g1 + proteins_v[1] * v2 + proteins_g[1] * g2 + proteins_v[2] * v3 + proteins_g[2] * g3 + proteins_v[3] * v4 + prt_ch * c >= Total_prt/4  # protein
        lpp_l += fat_ms*ms + fats_ec * br + fat_v[0] * v1 + fat_g[0] * g1 + fat_v[1] * v2 + fat_g[1] * g2 + fat_v[2] * v3 + fat_g[2] * g3 + fat_v[3] * v4 + fat_ch * c >= 11  # fats
        #lpp_l += carb_ms*ms + carb_ec * br + carbs_v[0] * v1 + carbs_g[0] * g1 + carbs_v[1] * v2 + carbs_g[1] * g2 + carbs_v[2] * v3 + carbs_g[2] * g3 + carbs_v[3] * v4 + carbs_g[3] * g4 + carb_ch * c <= .65 * Total_cal_bf  # carb
        lpp_l += ms_cal*ms + cal_ec * br + calorie_v[0] * v1 + calorie_g[0] * g1 + calorie_v[1] * v2 + calorie_g[1] * g2 + calorie_v[2] * v3 + calorie_g[2] * g3 + calorie_v[3] * v4 + ch_cal * c >= Total_cal_l  # Calories
        #lpp_l += prt_ms*ms + prt_ec * br + proteins_v[0] * v1 + proteins_g[0] * g1 + proteins_v[1] * v2 + proteins_g[1] * g2 + proteins_v[2] * v3 + proteins_g[2] * g3 + proteins_v[3] * v4 + proteins_g[3] * g4 + prt_ch * c <= 0.35 * Total_cal_bf  # protein
        lpp_l += fat_ms*ms + fats_ec * br + fat_v[0] * v1 + fat_g[0] * g1 + fat_v[1] * v2 + fat_g[1] * g2 + fat_v[2] * v3 + fat_g[2] * g3 + fat_v[3] * v4 + fat_ch * c <= 20  # fats
        lpp_l += g1 >= 0.5
        lpp_l += g2 >= 0.5
        lpp_l += g3 >= 0.5
        lpp_l += v1 >= 0.5
        lpp_l += v2 >= 0.5
        lpp_l += v3 >= 0.5
        lpp_l += v4 >= 0.5
        lpp_l += g1+g2+g3 <= 4
        lpp_l += v1 + v2 <= 3
        lpp_l += v3 + v4 <= 3
        lpp_l += c <=2
        if(ms_list != 'None'):
            pass
        else:
            lpp_l += ms >= 0.5
        lpp_l.solve()
        ans = pulp.LpStatus[lpp_l.status]
        print(ans)
        l_val = {}
        for variable in lpp_l.variables():
            print("{} = {}".format(variable.name, variable.varValue))
            if(variable.name == 'br'):
                l_val[ess_carbs] = variable.varValue
            elif(variable.name == 'ms' and ms_list!='None'):
                l_val[ms_list] = variable.varValue
            elif (variable.name == 'v1'):
                l_val[veg_list[0]] = variable.varValue
            elif (variable.name == 'v2'):
                l_val[veg_list[1]] = variable.varValue
            elif (variable.name == 'v3'):
                l_val[veg_list[2]] = variable.varValue
            elif (variable.name == 'v4'):
                l_val[veg_list[3]] = variable.varValue
            elif (variable.name == 'g1'):
                l_val[green_list[0]] = variable.varValue
            elif (variable.name == 'g2'):
                l_val[green_list[1]] = variable.varValue
            elif (variable.name == 'g3'):
                l_val[green_list[2]] = variable.varValue
            elif (variable.name == 'c' and c!='None'):
                l_val[chesse_type] = variable.varValue

        print(pulp.value(lpp_l.objective))
        cst_l = pulp.value(lpp_l.objective)
        session['cst_l'] = cst_l
        session['l_val'] = l_val
        return render_template('snack.html')

@app.route('/DINNER', methods=['POST','GET'])
def sn():
    #min_cal = 2400
    if(request.method == 'POST'):
        min_cal = int(session.get('min_cal', None))
        wt = float(session.get('wt', None))
        print(min_cal)
        lpp_s = pulp.LpProblem("My LP Problem", pulp.LpMinimize)
        f1 = pulp.LpVariable('f1', lowBound=0, cat='Continuous') #Fruit 1
        f2 = pulp.LpVariable('f2', lowBound=0, cat='Continuous') #Fruit 2
        f3 = pulp.LpVariable('f3', lowBound=0, cat='Continuous') #Fruit 3
        f4 = pulp.LpVariable('f4', lowBound=0, cat='Continuous') #Fruit 4
        bs = pulp.LpVariable('bs', lowBound=0, cat='Continuous') #Bread
        bv = pulp.LpVariable('bv', lowBound=0, cat='Continuous') #Beverage
        n = pulp.LpVariable('n', lowBound=0, cat='Continuous') #Mixed nuts
        calorie = []
        fat = []
        carbs = []
        proteins = []
        cost = []
        df3 = pd.read_csv("C:\\Users\Aakanksha\\Documents\\MS CPE\\Spring 2018\\DietProblem_Solver\\NutritionalFacts.csv", encoding="utf8")
        df4 = df3.set_index("Food and Serving", drop= False)
        var_cnt = 0
        fruits = request.form.getlist("fruit_list")
        var_cnt=len(fruits)
        print(var_cnt)
        for i in range(0,len(fruits)):
            cal = df4.loc[fruits[i],"Calories"]
            price = df4.loc[fruits[i],"Cost"]
            carb = df4.loc[fruits[i],"Carbohydrate"]
            fats = df4.loc[fruits[i],"Total Fat"]
            prt = df4.loc[fruits[i],"Protein"]
            print(cal)
            calorie.append(cal)
            cost.append(price)
            carbs.append(carb)
            fat.append(fats)
            proteins.append(prt)
        for j in range(0,4-len(fruits)):
            calorie.append(0)
            cost.append(0)
            carbs.append(0)
            fat.append(0)
            proteins.append(0)
        bread = request.form.get("bread")
        if(bread!='None'):
            cal_bread = df4.loc[bread, "Calories"]
            # calorie.append(cal_bread)
            price_bread = df4.loc[bread, "Cost"]
            # cost.append(price_bread)
            carb_bread = df4.loc[bread, "Carbohydrate"]
            prt_bread = df4.loc[bread, "Protein"]
            fat_bread = df4.loc[bread, "Total Fat"]
        else:
            cal_bread = 0
            price_bread = 0
            carb_bread = 0
            prt_bread = 0
            fat_bread = 0
        beverage = request.form.get("beverage")
        cal_bev = df4.loc[beverage, "Calories"]
        #calorie.append(cal_bev)
        price_bev = df4.loc[beverage, "Cost"]
        #cost.append(price_bev)
        carb_bev = df4.loc[beverage,"Carbohydrate"]
        prt_bev = df4.loc[beverage,"Protein"]
        fat_bev = df4.loc[beverage,"Total Fat"]
        var_cnt += 2
        print(var_cnt)
        nuts = request.form.get("nuts")
        if(nuts!="None"):
            var_cnt+=1
            cal_nuts = df4.loc[nuts,"Calories"]
            #calorie.append(cal_meat)
            price_nuts = df4.loc[nuts, "Cost"]
            #cost.append(price_meat)
            carb_nuts = df4.loc[nuts, "Carbohydrate"]
            prt_nuts = df4.loc[nuts, "Protein"]
            fat_nuts = df4.loc[nuts, "Total Fat"]
        else:
            cal_nuts = 0
            price_nuts = 0
            carb_nuts = 0
            prt_nuts = 0
            fat_nuts = 0

        #print(fruits,bread,beverage,meat,eggs,oats,var_cnt)
        #print(calorie)

        # Objective function
        lpp_s += cost[0] * f1 + cost[1] * f2 + cost[2] * f3 + cost[3] * f4 + price_bread*bs + price_bev*bv + price_nuts*n, "Z"

        Total_cal_sn = 0.2*min_cal
        Total_prt = 0.37 *wt

        # contraints
        # lpp_s += carbs[0] * f1 + carbs[1]*f2 + carbs[2]*f3 + carbs[3] * f4 + carb_bread*bs + carb_bev*bv + carb_nuts*n >= 0.42*Total_cal_sn #carb
        # lpp_s += proteins[0] * f1 + proteins[1]*f2+proteins[2]*f3 + proteins[3] * f4 + prt_bread*bs + prt_bev*bv + prt_nuts*n  >= 0.10*Total_cal_sn #protein
        # lpp_s += fat[0] *f1 + fat[1] *f2 + fat[2]*f3 + fat[3] * f4 + fat_bread*bs + fat_bev*bv + fat_nuts*n >= .20*Total_cal_sn #fats
        # lpp_s += carbs[0] * f1 + carbs[1]*f2 + carbs[2]*f3 + carbs[3] * f4 + carb_bread*bs + carb_bev*bv + carb_nuts*n <= .65 * Total_cal_sn  # carb
        # lpp_s +=  calorie[0] * f1 + calorie[1]*f2 +calorie[2]*f3 + calorie[3] * f4 + cal_bread*bs + cal_bev*bv + cal_nuts*n >= Total_cal_sn # Calories
        # lpp_s += proteins[0] * f1 + proteins[1]*f2+proteins[2]*f3 + proteins[3] * f4 + prt_bread*bs + prt_bev*bv + prt_nuts*n <= 0.35 * Total_cal_sn  # protein
        # lpp_s += fat[0] *f1 + fat[1] *f2 + fat[2]*f3 + fat[3] * f4 + fat_bread*bs + fat_bev*bv + fat_nuts*n <= .35 * Total_cal_sn  # fats
        # lpp_s += bs <=2
        # lpp_s += bv <= 1
        # lpp_s += n <= 0.2
        # lpp_s += f1 >= 0.5
        # lpp_s += f2 >= 0.5
        # lpp_s += f3 >= 0.5
        # lpp_s += f4 >= 0.5

        lpp_s += carbs[0] * f1 + carbs[1] * f2 + carbs[2] * f3 + carbs[3] * f4 >= 15  # carb
        lpp_s += carb_bread * bs + carb_bev * bv + carb_nuts * n >= 25  # carb
        lpp_s += carbs[0] * f1 + carbs[1] * f2 + carbs[2] * f3 + carbs[3] * f4 <= 35  # carb
        lpp_s += carb_bread * bs + carb_bev * bv + carb_nuts * n <= 60  # carb
        lpp_s += proteins[0] * f1 + proteins[1] * f2 + proteins[2] * f3 + proteins[3] * f4 + prt_bread * bs + prt_bev * bv + prt_nuts * n >= Total_prt / 4  # protein
        lpp_s += fat[0] * f1 + fat[1] * f2 + fat[2] * f3 + fat[3] * f4 + fat_bread * bs + fat_bev * bv + fat_nuts * n >= 11  # fats
        lpp_s += fat[0] * f1 + fat[1] * f2 + fat[2] * f3 + fat[3] * f4 + fat_bread * bs + fat_bev * bv + fat_nuts * n <= 20  # fats
        lpp_s += calorie[0] * f1 + calorie[1] * f2 + calorie[2] * f3 + calorie[3] * f4 + cal_bread * bs + cal_bev * bv + cal_nuts * n >= Total_cal_sn  # Calories
        lpp_s += bs >=0
        lpp_s += bs <=2
        lpp_s += f1 >=0
        lpp_s += f2 >=0
        lpp_s += f3 >= 0
        lpp_s += f4 >= 0
        lpp_s += f1 + f2 + f3 + f4 >= 0.5
        lpp_s += f1 + f2 +f3 + f4 <=4
        lpp_s.solve()
        ans = pulp.LpStatus[lpp_s.status]
        print(ans)
        s_val = {}
        for variable in lpp_s.variables():
            print("{} = {}".format(variable.name, variable.varValue))
            if (variable.name == 'f1'):
                s_val[fruits[0]] = variable.varValue
            elif (variable.name == 'f2'):
                s_val[fruits[1]] = variable.varValue
            elif (variable.name == 'f3'):
                s_val[fruits[2]] = variable.varValue
            elif (variable.name == 'f4'):
                s_val[fruits[3]] = variable.varValue
            elif (variable.name == 'bs' and bread!='None'):
                s_val[bread] = variable.varValue
            elif (variable.name == 'bv'):
                s_val[beverage] = variable.varValue
            elif (variable.name == 'n' and n!='None'):
                s_val[nuts] = variable.varValue
        session['s_val'] = s_val

        print(pulp.value(lpp_s.objective))
        cst_s = pulp.value(lpp_s.objective)
        session['cst_s'] = cst_s

        return render_template('dinner.html')

@app.route('/RESULT', methods=['POST','GET'])
def dinner():
    if(request.method == 'POST'):
        i =0
        j = 0
        k = 0
        l = 0
        min_cal = int(session.get('min_cal', None))
        wt = float(session.get('wt', None))
        lpp_d = pulp.LpProblem("My LP Problem", pulp.LpMinimize)
        brd = pulp.LpVariable('brd', lowBound=0, cat='Continuous')  # carb essential
        msd = pulp.LpVariable('msd', lowBound=0, cat='Continuous')  # meat and sea food
        v1d = pulp.LpVariable('v1d', lowBound=0, cat='Continuous')  # veggie 1
        v2d = pulp.LpVariable('v2d', lowBound=0, cat='Continuous')  # veggie 2
        v3d = pulp.LpVariable('v3d', lowBound=0, cat='Continuous')  # veggie 3
        v4d = pulp.LpVariable('v4d', lowBound=0, cat='Continuous')  # veggie 4
        g1d = pulp.LpVariable('g1d', lowBound=0, cat='Continuous')  # green 1
        g2d = pulp.LpVariable('g2d', lowBound=0, cat='Continuous')  # green 2
        g3d = pulp.LpVariable('g3d', lowBound=0, cat='Continuous')  # green 3
        #g4d = pulp.LpVariable('g4d', lowBound=0, cat='Continuous')  # green 4
        cd = pulp.LpVariable('cd', lowBound=0, cat='Continuous')  # cheese
        cost_v = []
        calorie_v = []
        fat_v = []
        carbs_v = []
        proteins_v = []
        cost_g = []
        calorie_g = []
        fat_g = []
        carbs_g = []
        proteins_g = []
        df3 = pd.read_csv("C:\\Users\Aakanksha\\Documents\\MS CPE\\Spring 2018\\DietProblem_Solver\\NutritionalFacts.csv",encoding="utf8")
        df4 = df3.set_index("Food and Serving", drop=False)
        ess_carbs = request.form.get("carb_list")
        ms_list = request.form.get("ms_list")
        veg_list = request.form.getlist("veggie_list")
        green_list = request.form.getlist("green_list")
        chesse_type = request.form.get("cheese_list")

        cal_ec = df4.loc[ess_carbs,"Calories"]
        price_ec = df4.loc[ess_carbs,"Cost"]
        carb_ec = df4.loc[ess_carbs,"Carbohydrate"]
        fats_ec = df4.loc[ess_carbs,"Total Fat"]
        prt_ec = df4.loc[ess_carbs,"Protein"]
        print(cal_ec)
        for i in range(0,len(veg_list)):
            cal_v = df4.loc[veg_list[i],"Calories"]
            price_v = df4.loc[veg_list[i],"Cost"]
            carb_v = df4.loc[veg_list[i],"Carbohydrate"]
            fats_v = df4.loc[veg_list[i],"Total Fat"]
            prt_v = df4.loc[veg_list[i],"Protein"]
            print(cal_v)
            calorie_v.append(cal_v)
            cost_v.append(price_v)
            carbs_v.append(carb_v)
            fat_v.append(fats_v)
            proteins_v.append(prt_v)
        for j in range(0,4-len(veg_list)):
            calorie_v.append(0)
            cost_v.append(0)
            carbs_v.append(0)
            fat_v.append(0)
            proteins_v.append(0)
        for k in range(0,len(green_list)):
            cal_g = df4.loc[green_list[k],"Calories"]
            price_g = df4.loc[green_list[k],"Cost"]
            carb_g = df4.loc[green_list[k],"Carbohydrate"]
            fats_g = df4.loc[green_list[k],"Total Fat"]
            prt_g = df4.loc[green_list[k],"Protein"]
            print(cal_g)
            calorie_g.append(cal_g)
            cost_g.append(price_g)
            carbs_g.append(carb_g)
            fat_g.append(fats_g)
            proteins_g.append(prt_g)
        for l in range(0,3-len(green_list)):
            calorie_g.append(0)
            cost_g.append(0)
            carbs_g.append(0)
            fat_g.append(0)
            proteins_g.append(0)
        if(ms_list == 'None'):
            ms_cal = 0
            price_ms = 0
            carb_ms = 0
            prt_ms = 0
            fat_ms = 0

        else:
            ms_cal = df4.loc[ms_list, "Calories"]
            # calorie.append(cal_bread)
            price_ms = df4.loc[ms_list, "Cost"]
            # cost.append(price_ms)
            carb_ms = df4.loc[ms_list, "Carbohydrate"]
            prt_ms = df4.loc[ms_list, "Protein"]
            fat_ms = df4.loc[ms_list, "Total Fat"]

        if(chesse_type == 'None'):
            ch_cal = 0
            price_ch = 0
            carb_ch = 0
            prt_ch = 0
            fat_ch = 0
        else:
            ch_cal = df4.loc[chesse_type, "Calories"]
            # calorie.append(cal_bread)
            price_ch = df4.loc[chesse_type, "Cost"]
            # cost.append(price_ms)
            carb_ch = df4.loc[chesse_type, "Carbohydrate"]
            prt_ch = df4.loc[chesse_type, "Protein"]
            fat_ch = df4.loc[chesse_type, "Total Fat"]
        print(len(green_list), len(veg_list))
        # Objective function
        lpp_d += price_ms *msd + price_ec * brd + cost_v[0] * v1d + cost_g[0] * g1d + cost_v[1] * v2d + cost_g[1] * g2d + cost_v[2] * v3d + cost_g[2] * g3d + cost_v[3] * v4d + price_ch * cd, "D"

        Total_cal_d = 0.2 * min_cal
        Total_prt = 0.37 * wt
        # contraints
        # lpp_d += carb_ms*msd + carb_ec * brd + carbs_v[0] * v1d + carbs_g[0] * g1d + carbs_v[1] * v2d + carbs_g[1] * g2d + carbs_v[2] * v3d + carbs_g[2] * g3d + carbs_v[3] * v4d + carbs_g[3] * g4d + carb_ch * cd >= 0.42 * Total_cal_d  # carb
        # lpp_d += prt_ms *msd + prt_ec * brd + proteins_v[0] * v1d + proteins_g[0] * g1d + proteins_v[1] * v2d + proteins_g[1] * g2d + proteins_v[2] * v3d + proteins_g[2] * g3d + proteins_v[3] * v4d + proteins_g[3] * g4d + prt_ch * cd >= 0.10 * Total_cal_d  # protein
        # lpp_d += fat_ms*msd + fats_ec * brd + fat_v[0] * v1d + fat_g[0] * g1d + fat_v[1] * v2d + fat_g[1] * g2d + fat_v[2] * v3d + fat_g[2] * g3d + fat_v[3] * v4d + fat_g[3] * g4d + fat_ch * cd >= .20 * Total_cal_d  # fats
        # lpp_d += carb_ms*msd + carb_ec * brd + carbs_v[0] * v1d + carbs_g[0] * g1d + carbs_v[1] * v2d + carbs_g[1] * g2d + carbs_v[2] * v3d + carbs_g[2] * g3d + carbs_v[3] * v4d + carbs_g[3] * g4d + carb_ch * cd <= .65 * Total_cal_d  # carb
        # lpp_d += ms_cal*msd + cal_ec * brd + calorie_v[0] * v1d + calorie_g[0] * g1d + calorie_v[1] * v2d + calorie_g[1] * g2d + calorie_v[2] * v3d + calorie_g[2] * g3d + calorie_v[3] * v4d + calorie_g[3] * g4d + ch_cal * cd >= Total_cal_d  # Calories
        # lpp_d += prt_ms*msd + prt_ec * brd + proteins_v[0] * v1d + proteins_g[0] * g1d + proteins_v[1] * v2d + proteins_g[1] * g2d + proteins_v[2] * v3d + proteins_g[2] * g3d + proteins_v[3] * v4d + proteins_g[3] * g4d + prt_ch * cd <= 0.35 * Total_cal_d  # protein
        # lpp_d += fat_ms*msd + fats_ec * brd + fat_v[0] * v1d + fat_g[0] * g1d + fat_v[1] * v2d + fat_g[1] * g2d + fat_v[2] * v3d + fat_g[2] * g3d + fat_v[3] * v4d + fat_g[3] * g4d + fat_ch * cd <= .35 * Total_cal_d  # fats
        # lpp_d += brd <= 2
        # lpp_d += g1d + g2d + g3d + g4d <= 100
        # lpp_d += v1d + v2d + v3d + v4d <= 100
        # lpp_d += msd <= 4
        # lpp_d += cd <= 10
        # lpp_d += g1d >= 0.5
        # lpp_d += g2d >= 0.5
        # lpp_d += g3d >= 0.5
        # lpp_d += g4d >= 0.5
        # lpp_d += v1d >= 0.5
        # lpp_d += v2d >= 0.5
        # lpp_d += v3d >= 0.5
        # lpp_d += v4d >= 0.5

        lpp_d += carb_ms * msd + carb_ec * brd + carb_ch * cd >= 15  # carb
        lpp_d += carbs_v[0] * v1d + carbs_g[0] * g1d + carbs_v[1] * v2d + carbs_g[1] * g2d + carbs_v[2] * v3d + carbs_g[2] * g3d + carbs_v[3] * v4d >= 15
        lpp_d += carb_ms * msd + carb_ec * brd + carb_ch * cd <= 40  # carb
        lpp_d += carbs_v[0] * v1d + carbs_g[0] * g1d + carbs_v[1] * v2d + carbs_g[1] * g2d + carbs_v[2] * v3d + carbs_g[2] * g3d + carbs_v[3] * v4d >= 30
        lpp_d += prt_ms * msd + prt_ec * brd + proteins_v[0] * v1d + proteins_g[0] * g1d + proteins_v[1] * v2d + proteins_g[1] * g2d + proteins_v[2] * v3d + proteins_g[2] * g3d + proteins_v[3] * v4d + prt_ch * cd >= Total_prt / 4  # protein
        lpp_d += fat_ms * msd + fats_ec * brd + fat_v[0] * v1d + fat_g[0] * g1d + fat_v[1] * v2d + fat_g[1] * g2d + fat_v[2] * v3d + fat_g[2] * g3d + fat_v[3] * v4d + fat_ch * cd >= 11  # fats
        # lpp_l += carb_ms*ms + carb_ec * br + carbs_v[0] * v1 + carbs_g[0] * g1 + carbs_v[1] * v2 + carbs_g[1] * g2 + carbs_v[2] * v3 + carbs_g[2] * g3 + carbs_v[3] * v4 + carbs_g[3] * g4 + carb_ch * c <= .65 * Total_cal_bf  # carb
        lpp_d += ms_cal * msd + cal_ec * brd + calorie_v[0] * v1d + calorie_g[0] * g1d + calorie_v[1] * v2d + calorie_g[1] * g2d + calorie_v[2] * v3d + calorie_g[2] * g3d + calorie_v[3] * v4d + ch_cal * cd >= Total_cal_d  # Calories
        # lpp_l += prt_ms*ms + prt_ec * br + proteins_v[0] * v1 + proteins_g[0] * g1 + proteins_v[1] * v2 + proteins_g[1] * g2 + proteins_v[2] * v3 + proteins_g[2] * g3 + proteins_v[3] * v4 + proteins_g[3] * g4 + prt_ch * c <= 0.35 * Total_cal_bf  # protein
        lpp_d += fat_ms * msd + fats_ec * brd + fat_v[0] * v1d + fat_g[0] * g1d + fat_v[1] * v2d + fat_g[1] * g2d + fat_v[2] * v3d + fat_g[2] * g3d + fat_v[3] * v4d + fat_ch * cd <= 20  # fats
        lpp_d += g1d >= 0.5
        lpp_d += g2d >= 0.5
        lpp_d += g3d >= 0.5
        lpp_d += v1d >= 0.5
        lpp_d += v2d >= 0.5
        lpp_d += v3d >= 0.5
        lpp_d += v4d >= 0.5
        lpp_d += g1d + g2d + g3d <= 4
        lpp_d += v1d + v2d <= 3
        lpp_d += v3d + v4d <= 3
        lpp_d += cd <= 2
        if (ms_list != 'None'):
            pass
        else:
            lpp_d += msd >= 0.5
        lpp_d.solve()
        ans = pulp.LpStatus[lpp_d.status]
        print(ans)
        d_val = {}
        for variable in lpp_d.variables():
            print("{} = {}".format(variable.name, variable.varValue))
            if (variable.name == 'brd'):
                d_val[ess_carbs] = variable.varValue
            elif (variable.name == 'msd' and ms_list!='None'):
                d_val[ms_list] = variable.varValue
            elif (variable.name == 'v1d'):
                d_val[veg_list[0]] = variable.varValue
            elif (variable.name == 'v2d'):
                d_val[veg_list[1]] = variable.varValue
            elif (variable.name == 'v3d'):
                d_val[veg_list[2]] = variable.varValue
            elif (variable.name == 'v4d'):
                d_val[veg_list[3]] = variable.varValue
            elif (variable.name == 'g1d'):
                d_val[green_list[0]] = variable.varValue
            elif (variable.name == 'g2d'):
                d_val[green_list[1]] = variable.varValue
            elif (variable.name == 'g3d'):
                d_val[green_list[2]] = variable.varValue
            elif (variable.name == 'cd' and chesse_type!='None'):
                d_val[chesse_type] = variable.varValue

        print(pulp.value(lpp_d.objective))
        cst_d = pulp.value(lpp_d.objective)
        bfcost = session.get('bfcost', None)
        bf_val = session.get('bf_val', None)
        cst_l = session.get('cst_l', None)
        l_val = session.get('l_val', None)
        cst_s = session.get('cst_s', None)
        s_val = session.get('s_val', None)
        total = bfcost + cst_l +cst_s + cst_d
        # for p,q in enumerate(bf_val):
        #     print(q + "=" + str(bf_val[q]))
        return render_template('result.html', bfcost=str(round(bfcost,3)), bf_val=bf_val, cst_l = str(round(cst_l,3)), l_val=l_val, cst_s = str(round(cst_s,3)), s_val =s_val, cst_d = str(round(cst_d,3)),d_val=d_val, total = str(round(total,3)))


if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.secret_key = 'dietproblem'
    app.run(host=host, port=port)
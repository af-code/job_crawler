from flask import Flask, request, render_template
from flask.helpers import url_for
from DatabaseConnector import DatabaseConnector
from AnalyticsConnector import AnalyticsConnector
from MainCrawler import MainCrawler
from datetime import date, datetime

main_crawler = MainCrawler()
analytics_connector = AnalyticsConnector()
database_connector = DatabaseConnector()
app = Flask(__name__)

@app.route('/')
def start():
    return render_template('table.html') 

@app.route('/start')
def submit_form():
    return render_template('start.html')

@app.route('/start', methods = ['POST', 'GET'])
def form_post():
    if request.method == 'POST':
        ok_list = []
        job = request.form.get("job")
        city = request.form.get("city")
        radius = str(request.form.get("radius"))
        if(job != "" and city != "" and radius != ""):
            if(request.form.get('switchIndeed') == "on"): 
                ok_list.append("indeed")

            if(request.form.get('switchMonster') == "on"):
                ok_list.append("monster")

            if(request.form.get('switchLinkedIn') == "on"):
                ok_list.append("linkedIn")
            
            if(request.form.get('switchStepStone') == "on"):
                ok_list.append("stepstone")

            for i in ok_list:
                main_crawler.start_crawler(i, job, city, radius)
            rows = database_connector.get_all_data("Indeed")
            return render_template('table.html', rows = rows)
        else:
            return render_template('start.html')

@app.route('/<item>', methods = ['GET'])
def update_table(item):
    if item != 'favicon.ico' and not item == 'table':
        rows = database_connector.get_all_data(format(item))
        return render_template('table.html', rows = rows)
    else:
        return render_template('table.html')

@app.route('/analytics')
def analytics_form():
    return(render_template('analytics.html')) 

@app.route('/analytics', methods = ['GET', 'POST'])
def show_list():
    if request.method == 'POST' and "analyze" in request.form:
        database_connector.delete_temp_data()
        
        ok_list = []
        job = request.form.get("job")
        city = request.form.get("city")
        radius = request.form.get("radius")
        try:
            start_date = date(int(request.form.get("startYear")), int(request.form.get("startMonth")), int(request.form.get("startDay"))) 
        except (ValueError, TypeError):
            start_date = date(2000, 1, 1)
        
        try:
            end_date = date(int(request.form.get("endYear")), int(request.form.get("endMonth")), int(request.form.get("endDay"))) 
        except (ValueError, TypeError):
            end_date = date(datetime.now())
        if(job != ""):
            if(request.form.get('switchIndeed') == "on"): 
                ok_list.append("Indeed")

            if(request.form.get('switchMonster') == "on"):
                ok_list.append("Monster")

            if(request.form.get('switchLinkedIn') == "on"):
                ok_list.append("LinkedIn")
            
            if(request.form.get('switchStepStone') == "on"):
                ok_list.append("Stepstone")

            ret_dict = analytics_connector.common_words(ok_list, job, city, radius, start_date, end_date)
            database_connector.insert_in_temp_table('Nouns', ret_dict["nouns"])
            database_connector.insert_in_temp_table('Verbs', ret_dict["verbs"])
            database_connector.insert_in_temp_table('Propn', ret_dict["propn"])
            database_connector.insert_in_temp_table('Nums', ret_dict["nums"])
            database_connector.insert_in_temp_table('Counter', ret_dict["counter"])

            nouns = database_connector.get_all_temp_data('Nouns')
            counter = database_connector.get_all_temp_data('Counter')[0]['content']
            return render_template('list.html', list = nouns, counter = counter)
        else:
            return render_template('analytics.html')

    elif request.method == 'POST' and "nouns" in request.form:
            nouns = database_connector.get_all_temp_data('Nouns')
            counter = database_connector.get_all_temp_data('Counter')[0]['content']
            return render_template('list.html', list = nouns, counter = counter)
    elif request.method == 'POST' and "verbs" in request.form:
            verbs = database_connector.get_all_temp_data('Verbs')
            counter = database_connector.get_all_temp_data('Counter')[0]['content']
            return render_template('list.html', list = verbs, counter = counter)
    elif request.method == 'POST' and "propn" in request.form:
            propn = database_connector.get_all_temp_data('Propn')
            counter = database_connector.get_all_temp_data('Counter')[0]['content']
            return render_template('list.html', list = propn, counter = counter)
    elif request.method == 'POST' and "nums" in request.form:
            nums = database_connector.get_all_temp_data('Nums')
            counter = database_connector.get_all_temp_data('Counter')[0]['content']
            return render_template('list.html', list = nums, counter = counter)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001) 
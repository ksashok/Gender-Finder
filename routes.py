from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from forms import NameCheck
from collections import Counter

app = Flask(__name__)
app.secret_key = "development-key"

##app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gender'
engine = create_engine('postgresql://localhost/gender')

@app.route("/genderapp", methods =['GET', 'POST'])
def findGender():
    form = NameCheck()
    check_Name = form.name.data

    if request.method == 'POST':
        result = engine.execute(
        '''
        SELECT gender,ethnicity FROM genderdata
        WHERE LOWER(name) = LOWER(%s)
        ''',
        (check_Name)

        )

        li = []
        eth = []
        for r in result:
            li.append(r.gender)
            eth.append(r.ethnicity.lower())

        c = Counter(eth)
        eth_final = c.most_common(1)

        male = li.count('M') + li.count('m')
        female = li.count('F') + li.count('f')
        if male == 0 and female == 0:
            return ("Sorry. Can't determine at this moment")
        male_percentage = (male / (male+female)) * 100
        female_percentage = 100 - male_percentage

        return (check_Name+" is "+ str("{0:.2f}".format(male_percentage)) +"% Male and " + str("{0:.2f}".format(female_percentage)) + "% Female"+"\n and is probably " + str(eth_final[0][0]).capitalize())

    elif request.method == 'GET':
            return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

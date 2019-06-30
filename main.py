from flask import Flask, flash, redirect, render_template, request, session,json

from inventory import Database

app = Flask(__name__)
app.secret_key="there is a coder"

db= Database()

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method=="POST":
        term = request.form.get('term')
        if term:
            record = Database().search(term)
            print(record)
            if record:
                flash('search complete','alert-success')
                return render_template('index.html',records=record)
            else:
                flash('could not find any result, loading all items ','alert-danger')
    data = Database().viewAll()
    # print(data)
    return render_template('index.html',records=data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method=="POST":
        name = request.form.get('name')
        price = request.form.get('price')
        qty = request.form.get('qty')
        qty=int(qty)
        price=float(price)
        status = Database().add(name,qty,price)
        if status:
            flash('successfully added','alert-success')
        else:
            flash('failed to add item','alert-danger')
        return redirect('/add')
    return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method=="POST":
        id = request.form.get('id')
        name = request.form.get('name')
        price = request.form.get('price')
        qty = request.form.get('qty')
        qty=int(qty)
        price=float(price)
        status = Database().edit(id,name,qty,price)
        if status:
            flash(f'successfully updated item {name} with id {id}','alert-success')
        else:
            flash('failed to update item','alert-danger')
        return redirect('/')
    elif request.method=='GET':
        id = request.args.get('i')
        if id:
            record= Database().viewById(id)
            flash(f'loaded data with id {id}','alert-success')
            return render_template('edit.html',records=record)
        else:
            flash('error finding item,please refresh','alert-warning')
            return redirect('/')



@app.route('/delete', methods=['GET'])
def delete():
    if request.method=="GET":
        id = request.args.get('i')
        if id:
            status= Database().delete(id)
            flash(f'deleted data with {id}','alert-success')
        else:
            flash('error deleting item,please refresh','alert-warning')
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)

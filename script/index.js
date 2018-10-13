let totals=[],
    users={
        'user':{'password':'password','role':'sale attendant'},
        'admin':{'password':'password','role':'admin'}
    }

function row_adder(table_name) {
    let id,rows= [],
    table = document.querySelector('tbody.table_body')
    id = table.children.length

    rows[0]=`
    <tr id="${id}" class="row">
        <td class="colunm id"><input class="cell" type="number" onChange="auto_row_adder()"></td>
        <td class="colunm name"><input class="cell" type="text" onChange="auto_row_adder()"></td>
        <td class="colunm cost"><input class="cell" type="text" onChange="auto_row_adder()"></td>
        <td class="colunm amount"><input class="cell" type="number" min="1" onChange="auto_row_adder()"></td>
        <td class="colunm total_cost"><input class="cell" type="text" readonly></td>
    </tr>
    `
    if (table_name == 'pos') {
        table.insertAdjacentHTML("beforeend",rows[0])
    }
}

function row_sum(cost, amount, row, id) {
    let total_cost, total

    if (cost && amount){
        total = cost*amount
        total_cost = row.querySelector('td.total_cost').querySelector('input.cell')
        total_cost.value = total
        totals[id]=total
    }
}

function auto_row_adder() {
    let  id, name, cost, amount, row, grand_total,
    rows=document.querySelectorAll('tr.row')
    for (row of rows) {
        id = row.querySelector('td.id').querySelector('input.cell').value
        name = row.querySelector('td.name').querySelector('input.cell').value
        cost = row.querySelector('td.cost').querySelector('input.cell').value
        amount = row.querySelector('td.amount').querySelector('input.cell').value
        if (id && name && cost && amount) {
            row_sum(cost, amount, row, id)
        }else{
            return null
        }
        grand_total= totals.reduce((sum, num) =>{
            return sum + num
        })
        document.querySelector('span.grand_total').innerHTML = grand_total
    }
    if (amount) {
        row_adder('pos')
    }
}

function login() {
    let user,form,username,password,destiation

    form=document.querySelector('form#login')
    username=form.querySelector('input#username.input').value
    password=form.querySelector('input#password.input').value

    if (users.hasOwnProperty(username)) {
        user = users[username]
        if (user.password=password) {
            destiation=(user.role=='sale attendant')?'pos.html':(user.role=='admin')?'inventory_manager.html':'#'
            location=destiation
        }
    }
}
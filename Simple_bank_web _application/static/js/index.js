
function showSection(id) {
  const all = document.querySelectorAll('.box-cont > div');
  all.forEach(div => div.classList.remove('show'));
  const el = document.getElementById(id);
  if (el) el.classList.add('show');
}

function depositFunds() {
            const amount = parseFloat(document.getElementById('deposit_amount').value);
            fetch('/deposit_ajax', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({amount: amount})
            })
            .then(res => res.json())
            .then(data => {
                if(data.new_balance !== undefined){
                    document.getElementById('current_balance').innerText = data.new_balance;
                    alert('Deposit successful!');
                    document.getElementById('deposit_amount').value = '';
                }
            });
        }
        
        function withdrawFunds() {
            const amount = parseFloat(document.getElementById('withdraw_amount').value);
            fetch('/withdraw_ajax', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({amount: amount})
            })
            .then(res => res.json())
            .then(data => {
                if(data.error){
                    alert(data.error);
                } else {
                    document.getElementById('current_balance').innerText = data.new_balance;
                    alert('Withdrawal successful!');
                    document.getElementById('withdraw_amount').value = '';
                }
            });
        }

        function transferFunds() {
            const receiver = document.getElementById('transfer_receiver').value;
            const amount = parseFloat(document.getElementById('transfer_amount').value);
            fetch('/transfer_ajax', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({receiver: receiver, amount: amount})
            })
            .then(res => res.json())
            .then(data => {
                if(data.error){
                    alert(data.error);
                } else {
                    document.getElementById('current_balance').innerText = data.new_balance;
                    alert('Transfer successful!');
                    document.getElementById('transfer_receiver').value = '';
                    document.getElementById('transfer_amount').value = '';
                }
            });
        }
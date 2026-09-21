<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My Tracking — Red H Checkpoints</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f3f6fa;color:#172033}
button,input,select{font:inherit}
button{cursor:pointer;border:0}
.welcome{position:fixed;inset:0;background:linear-gradient(135deg,#dbeafe,#ecfdf5);display:flex;align-items:center;justify-content:center;z-index:100}
.welcome-card{width:min(620px,92%);background:white;border-radius:28px;padding:60px 30px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.15)}
.welcome-icon{font-size:70px}.welcome h1{font-size:42px;margin:15px 0 10px}.welcome p{color:#667085;margin-bottom:30px}
.start{background:#2563eb;color:white;padding:14px 60px;border-radius:10px;font-weight:700}
.app{display:none;min-height:100vh}
.sidebar{position:fixed;left:0;top:0;bottom:0;width:245px;background:#111827;color:white;padding:18px 12px;display:flex;flex-direction:column;z-index:10}
.brand{font-weight:800;font-size:18px;padding:10px 12px 25px}
.nav{width:100%;background:transparent;color:#d1d5db;text-align:left;padding:13px 14px;border-radius:9px;margin:2px 0;font-weight:600}
.nav:hover,.nav.active{background:#263244;color:white}.side-bottom{margin-top:auto}
.main{margin-left:245px;padding:25px;min-height:100vh}.inner{max-width:1100px;margin:auto}
.page{display:none}.page.active{display:block}
.card{background:white;border-radius:15px;padding:22px;margin:16px 0;box-shadow:0 3px 15px rgba(0,0,0,.06)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}
.tile{background:white;border-radius:14px;padding:24px;text-align:left;box-shadow:0 3px 15px rgba(0,0,0,.06);width:100%}
.tile:hover{outline:2px solid #93c5fd}.tile-icon{font-size:30px}.tile b{display:block;margin:10px 0 5px}.muted{color:#667085;font-size:13px}
.count{font-size:48px;font-weight:800;font-variant-numeric:tabular-nums}
.primary{background:#2563eb;color:white;padding:11px 16px;border-radius:8px;font-weight:700}
.secondary{background:#eef2f7;color:#172033;padding:10px 15px;border-radius:8px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
label{display:block;font-size:13px;font-weight:700;margin:10px 0}
input,select{display:block;width:100%;margin-top:6px;padding:10px;border:1px solid #d0d5dd;border-radius:7px;background:white}
.actions{display:flex;gap:9px;justify-content:flex-end;margin-top:16px}
.schedule{display:grid;gap:9px}.time-block{background:white;border-left:5px solid #2563eb;padding:13px;border-radius:8px;display:flex;justify-content:space-between}
.time-block.current{background:#eff6ff;outline:2px solid #93c5fd}
.delete{background:#fee2e2;color:#991b1b;padding:6px 9px;border-radius:6px;height:max-content}
.money-options{margin-top:20px}
.money-module{display:none}
.option-grid{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:15px}
.option{background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:22px;text-align:left}
.option:hover{outline:2px solid #93c5fd}
.option-icon{font-size:30px}
.tools-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:200;align-items:center;justify-content:center;padding:20px}
.modal-box{background:white;border-radius:15px;width:min(800px,96%);max-height:90vh;overflow:auto;padding:22px}
.modal-head{display:flex;justify-content:space-between;align-items:center}
.modal-head button{background:#eef2f7;border-radius:7px;padding:7px}
.tool-group{border:1px solid #e5e7eb;border-radius:10px;padding:12px;margin:10px 0}
.tool-group h3{margin:0 0 10px}.tool-row{display:flex;justify-content:space-between;padding:6px 0;border-top:1px solid #f0f0f0}
.remove{background:#fee2e2;color:#991b1b;padding:5px 8px;border-radius:5px;font-size:12px}
.add-row{display:flex;gap:7px;margin-top:8px}.add-row input{margin:0}.add-row button{background:#2563eb;color:white;padding:8px 12px;border-radius:7px}
.note{background:#eff6ff;padding:12px;border-radius:8px;color:#344054;font-size:13px;margin-top:12px}
@media(max-width:750px){.sidebar{width:70px}.brand span,.nav span{display:none}.nav{text-align:center;font-size:20px}.main{margin-left:70px}.grid,.option-grid,.form-grid{grid-template-columns:1fr}.welcome h1{font-size:32px}}

.upload-window{display:none;position:fixed;inset:0;background:rgba(15,23,42,.72);z-index:300;align-items:center;justify-content:center;padding:20px}
.upload-window-box{width:min(820px,96vw);max-height:92vh;overflow:auto;background:#f8fafc;border-radius:20px;padding:24px;box-shadow:0 25px 70px rgba(0,0,0,.3)}
.upload-window-head{display:flex;justify-content:space-between;align-items:flex-start;gap:15px}
.upload-window-head h2{margin:0 0 5px}.upload-close{background:#e5e7eb;border-radius:9px;padding:9px 12px;font-size:18px}
.upload-choice-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
.upload-choice{background:white;border:2px solid transparent;border-radius:16px;padding:28px;text-align:left;box-shadow:0 4px 16px rgba(0,0,0,.06)}
.upload-choice:hover{border-color:#93c5fd;transform:translateY(-2px)}
.upload-choice-icon{font-size:38px;margin-bottom:12px}.upload-choice b{display:block;font-size:20px;margin-bottom:7px}.upload-choice span{color:#667085;font-size:14px}
#uploadWindowContent .card{box-shadow:none;border:1px solid #e5e7eb;margin-top:20px}
@media(max-width:650px){.upload-choice-grid{grid-template-columns:1fr}}

#sheetDataWindow .upload-window-box{width:min(1000px,96vw)}

.money-income-card{background:#ecfdf3!important;border:2px solid #22c55e}
.money-income-card b,.money-income-card #moneyIncome{color:#15803d}

.money-expense-card{background:#fff1f2!important;border:2px solid #ef4444}
.money-expense-card b,.money-expense-card #moneyExpenses{color:#dc2626}

.money-savings-card{background:#eff6ff!important;border:2px solid #3b82f6}
.money-savings-card b,.money-savings-card #moneySavings{color:#2563eb}

.money-loan-took-card{background:#fff7ed!important;border:2px solid #fb923c}
.money-loan-took-card b,.money-loan-took-card #moneyLoanTook{color:#c2410c}
.money-loan-gave-card{background:#f5f3ff!important;border:2px solid #8b5cf6}
.money-loan-gave-card b,.money-loan-gave-card #moneyLoanGave{color:#7c3aed}
.view-options-card{background:#f8fafc!important;border:2px solid #94a3b8}

.money-others-card{background:#f8fafc!important;border:2px solid #cbd5e1}
.money-others-card b{color:#334155}
.danger-choice{border-color:#fecaca!important;background:#fff7f7!important}
.danger-choice b{color:#b42318}

.set-main-group{background:white;border:1px solid #e5e7eb;border-radius:14px;padding:16px;margin:14px 0}
.set-main-head{display:flex;gap:10px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.set-main-title{font-size:18px;font-weight:800;min-width:130px}
.set-main-actions{display:flex;gap:7px}
.set-main-actions button{padding:7px 10px;border-radius:7px}
.rename-btn{background:#e0f2fe;color:#075985}
.delete-main-btn{background:#fee2e2;color:#991b1b}
.set-sub-row{display:flex;gap:8px;align-items:center;padding:8px 0;border-top:1px solid #f1f5f9}
.set-sub-row input{margin:0;flex:1}
.set-sub-row button{padding:6px 9px;border-radius:6px}
.set-add-sub{display:flex;gap:8px;margin-top:10px}
.set-add-sub input{margin:0;flex:1}
.set-add-sub button{background:#2563eb;color:#fff;padding:8px 12px;border-radius:7px}
.period-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}
.period-tab{background:#e5e7eb;color:#334155;padding:10px 18px;border-radius:999px;font-weight:700}
.period-tab.active{background:#2563eb;color:#fff}
.period-control-row{display:flex;gap:10px;align-items:end;flex-wrap:wrap}
.period-control-row label{margin:0;min-width:160px}
.view-summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 0}
.view-summary{background:#fff;border-radius:14px;padding:18px;box-shadow:0 3px 12px rgba(0,0,0,.06)}
.view-summary.income{border:2px solid #22c55e;background:#ecfdf3}
.view-summary.expense{border:2px solid #ef4444;background:#fff1f2}
.view-summary.saving{border:2px solid #3b82f6;background:#eff6ff}
.view-summary b{display:block;margin-bottom:8px}
.view-summary .amt{font-size:26px;font-weight:800}
@media(max-width:650px){.view-summary-grid{grid-template-columns:1fr}}

.money-remaining-card{background:#f0fdf4!important;border:2px solid #16a34a}
.money-remaining-card b,.money-remaining-card #moneyRemaining{color:#166534}

.report-columns{display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:14px;margin-top:14px}
.report-card{background:white;border-radius:14px;padding:14px;box-shadow:0 3px 12px rgba(0,0,0,.06);overflow:auto}
.report-card h3{margin:0 0 10px}
.report-card.income h3{background:#bbf7d0;padding:8px;border-radius:7px}
.report-card.expense h3{background:#fecaca;padding:8px;border-radius:7px}
.report-card.saving h3{background:#bfdbfe;padding:8px;border-radius:7px}
.report-table{width:100%;border-collapse:collapse;font-size:13px}
.report-table th,.report-table td{padding:7px;border-bottom:1px solid #e5e7eb;text-align:left}
.report-table th:nth-child(2),.report-table td:nth-child(2){text-align:right}
.report-table th:nth-child(3),.report-table td:nth-child(3){text-align:right}
.report-total{font-weight:800}
.overall-card{margin-top:14px;background:white;border-radius:14px;padding:14px;box-shadow:0 3px 12px rgba(0,0,0,.06)}
.overall-table{width:min(520px,100%);border-collapse:collapse}
.overall-table th,.overall-table td{padding:8px;border-bottom:1px solid #e5e7eb}
.overall-table th{background:#bbf7d0}
.overall-table td:nth-child(2),.overall-table td:nth-child(3){text-align:right}
@media(max-width:900px){.report-columns{grid-template-columns:1fr}}

.stock-choice-card{text-align:left}
.nifty-card{border:2px solid #3b82f6!important;background:#eff6ff!important}
.nse-card{border:2px solid #64748b!important;background:#f8fafc!important}
.stock-list-card{margin-top:20px}
.stock-list-head{display:flex;justify-content:space-between;gap:14px;align-items:center;flex-wrap:wrap}
.stock-list-head h2{margin:0}
.stock-search{width:min(320px,100%);margin:0}
.stock-symbol-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:9px;margin-top:16px}
.stock-symbol{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:11px;text-align:left}
.stock-symbol:hover{border-color:#60a5fa}
.stock-symbol b{display:block}
.stock-symbol span{font-size:11px;color:#64748b}

.nifty-card{border:2px solid #22c55e!important;background:#f0fdf4!important}
.nse-card{border:2px solid #3b82f6!important;background:#eff6ff!important}
.market-panel{margin-top:20px}
.market-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}
.market-head h2{margin:0 0 5px}
@media(max-width:700px){
    }

.market-safe-box{margin-top:18px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:38px;text-align:center}
.big-market-icon{font-size:58px;margin-bottom:12px}
.market-safe-box h3{margin:8px 0}
.market-safe-box p{color:#64748b;line-height:1.6}

.summary-table-card{margin-top:14px}
.summary-table{width:100%;border-collapse:collapse;font-size:12px;table-layout:fixed}
.summary-table th{background:#3b82f6;color:white;padding:7px 5px;border:1px solid #cbd5e1;text-align:center;white-space:normal;line-height:1.15}
.summary-table td{padding:7px 5px;border:1px solid #e2e8f0;text-align:right;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.summary-table td:first-child{text-align:left}
.summary-table td:nth-child(2){text-align:left}
.money-positive{color:#15803d;font-weight:700}
.money-negative{color:#dc2626;font-weight:700}
.money-saving{color:#2563eb;font-weight:700}

.category-total-columns{grid-template-columns:repeat(3,minmax(280px,1fr))}
@media(max-width:1000px){.category-total-columns{grid-template-columns:1fr 1fr}}
@media(max-width:700px){.category-total-columns{grid-template-columns:1fr}}

/* Option 2: keep all columns visible without horizontal swipe */
.summary-table th:nth-child(1),.summary-table td:nth-child(1){width:14%}
.summary-table th:nth-child(2),.summary-table td:nth-child(2){width:12%}
.summary-table th:nth-child(3),.summary-table td:nth-child(3){width:14%}
.summary-table th:nth-child(4),.summary-table td:nth-child(4){width:14%}
.summary-table th:nth-child(5),.summary-table td:nth-child(5){width:14%}
.summary-table th:nth-child(6),.summary-table td:nth-child(6){width:14%}
.summary-table th:nth-child(7),.summary-table td:nth-child(7){width:18%}

/* For Monthly/Yearly (6 columns), rebalance automatically */
.summary-table.compact-6 th:nth-child(1),.summary-table.compact-6 td:nth-child(1){width:16%}
.summary-table.compact-6 th:nth-child(2),.summary-table.compact-6 td:nth-child(2){width:16%}
.summary-table.compact-6 th:nth-child(3),.summary-table.compact-6 td:nth-child(3){width:16%}
.summary-table.compact-6 th:nth-child(4),.summary-table.compact-6 td:nth-child(4){width:16%}
.summary-table.compact-6 th:nth-child(5),.summary-table.compact-6 td:nth-child(5){width:16%}
.summary-table.compact-6 th:nth-child(6),.summary-table.compact-6 td:nth-child(6){width:20%}

@media(max-width:700px){
  .summary-table{font-size:10.5px}
  .summary-table th,.summary-table td{padding:6px 3px}
  .summary-table-card{padding:10px}
}

.sync-card{padding:14px 18px}
.sync-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}

.google-sync-panel{border:2px solid #93c5fd;background:#f8fbff}
.google-sync-row{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.google-sync-actions{display:flex;gap:8px;flex-wrap:wrap}
#googleSyncStatus{margin-top:5px;font-weight:600}

/* Clickable Money cards */
.money-income-card,.money-expense-card,.money-savings-card,
.money-loan-took-card,.money-loan-gave-card{cursor:pointer}
.money-income-card:hover,.money-expense-card:hover,.money-savings-card:hover,
.money-loan-took-card:hover,.money-loan-gave-card:hover{
  transform:translateY(-2px);
  box-shadow:0 8px 22px rgba(15,23,42,.12);
}

/* Category transaction window */
.category-transactions-box{width:min(1150px,97vw);max-height:92vh}
.category-filter-bar{margin:14px 0}
.category-filter-bar input{width:100%;margin:0}
.category-table-wrap{overflow:auto;max-height:68vh;border-radius:12px;border:1px solid #e2e8f0}
.category-transaction-table{width:100%;border-collapse:collapse;min-width:800px;background:#fff}
.category-transaction-table th{
  position:sticky;top:0;z-index:2;
  padding:10px 9px;text-align:left;border-bottom:1px solid #cbd5e1;
}
.category-transaction-table td{padding:9px;border-bottom:1px solid #e5e7eb}
.category-transaction-table .transaction-amount{text-align:right;font-weight:800}
.category-transaction-table.cat-income th{background:#dcfce7;color:#166534}
.category-transaction-table.cat-income .transaction-amount{color:#15803d}
.category-transaction-table.cat-expense th{background:#fee2e2;color:#991b1b}
.category-transaction-table.cat-expense .transaction-amount{color:#dc2626}
.category-transaction-table.cat-saving th{background:#dbeafe;color:#1d4ed8}
.category-transaction-table.cat-saving .transaction-amount{color:#2563eb}
.category-transaction-table.cat-loan-took th{background:#ffedd5;color:#9a3412}
.category-transaction-table.cat-loan-took .transaction-amount{color:#c2410c}
.category-transaction-table.cat-loan-gave th{background:#ede9fe;color:#6d28d9}
.category-transaction-table.cat-loan-gave .transaction-amount{color:#7c3aed}

.subcategory-tabs{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  margin:16px 0 8px;
}
.subcategory-tab{
  display:flex;
  flex-direction:column;
  gap:4px;
  min-width:120px;
  padding:10px 14px;
  border-radius:12px;
  background:#f8fafc;
  border:1px solid #cbd5e1;
  text-align:left;
}
.subcategory-tab:hover{
  border-color:#60a5fa;
}
.subcategory-tab.active{
  background:#2563eb;
  color:#fff;
  border-color:#2563eb;
}
.subcategory-tab span{
  font-size:12px;
  opacity:.85;
}

.money-set-main-tabs{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  margin:16px 0 18px;
}
.money-set-main-tab{
  min-width:130px;
  padding:12px 16px;
  border-radius:12px;
  background:#eef2f7;
  border:1px solid #cbd5e1;
  text-align:left;
  display:flex;
  flex-direction:column;
  gap:4px;
}
.money-set-main-tab b{
  font-size:15px;
}
.money-set-main-tab span{
  font-size:11px;
  color:#64748b;
}
.money-set-main-tab.active{
  background:#2563eb;
  color:#fff;
  border-color:#2563eb;
}
.money-set-main-tab.active span{
  color:#dbeafe;
}
.money-set-detail{
  margin-top:0;
}
.money-set-sub-list{
  margin-top:12px;
}

#moneySetSyncStatus{font-weight:700}

.cashflow-report-columns{grid-template-columns:repeat(3,minmax(260px,1fr))}
.report-card.loan-in h3{background:#e0f2fe;padding:8px;border-radius:7px;color:#075985}
.report-card.loan-out h3{background:#ffedd5;padding:8px;border-radius:7px;color:#9a3412}
.loan-in-amount{color:#0369a1;font-weight:700}
.loan-out-amount{color:#c2410c;font-weight:700}
.cashflow-summary-table{min-width:1180px}
@media(max-width:1000px){.cashflow-report-columns{grid-template-columns:1fr 1fr}}
@media(max-width:700px){.cashflow-report-columns{grid-template-columns:1fr}}

/* V44 - Compact View Options */
#viewOptionsWindow .upload-window-box,
#viewOptionsWindow .view-window-box{
  width:min(1500px,99vw)!important;
  max-width:1500px!important;
  max-height:96vh!important;
  padding:18px!important;
}

#viewOptionsWindow .upload-window-head{
  margin-bottom:8px!important;
}

#viewOptionsWindow .period-tabs{
  margin:10px 0!important;
  gap:6px!important;
}

#viewOptionsWindow .period-tab{
  padding:8px 14px!important;
  font-size:14px!important;
}

#viewOptionsWindow .view-summary-grid{
  gap:8px!important;
  margin:8px 0!important;
}

#viewOptionsWindow .view-summary{
  padding:12px 16px!important;
  min-height:auto!important;
}

#viewOptionsWindow .view-summary .amt{
  font-size:24px!important;
}

#viewOptionsWindow .summary-table-card{
  padding:12px!important;
  margin-top:8px!important;
}

#viewOptionsWindow .summary-table-card h3{
  margin:0!important;
}

#viewOptionsWindow .cashflow-summary-table{
  width:100%!important;
  min-width:0!important;
  table-layout:fixed!important;
  font-size:11px!important;
}

#viewOptionsWindow .cashflow-summary-table th{
  padding:6px 3px!important;
  line-height:1.05!important;
  white-space:normal!important;
  font-size:10.5px!important;
}

#viewOptionsWindow .cashflow-summary-table td{
  padding:6px 3px!important;
  font-size:10.5px!important;
  white-space:nowrap!important;
  overflow:hidden!important;
  text-overflow:ellipsis!important;
}

/* Daily: Date, Day, Income, Expenses, Saving, In, Out, Loan In, Loan Out, Others, Balance */
#viewOptionsWindow .cashflow-summary-table th:nth-child(1),
#viewOptionsWindow .cashflow-summary-table td:nth-child(1){width:10%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(2),
#viewOptionsWindow .cashflow-summary-table td:nth-child(2){width:7%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(3),
#viewOptionsWindow .cashflow-summary-table td:nth-child(3){width:9%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(4),
#viewOptionsWindow .cashflow-summary-table td:nth-child(4){width:9%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(5),
#viewOptionsWindow .cashflow-summary-table td:nth-child(5){width:9%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(6),
#viewOptionsWindow .cashflow-summary-table td:nth-child(6){width:7%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(7),
#viewOptionsWindow .cashflow-summary-table td:nth-child(7){width:7%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(8),
#viewOptionsWindow .cashflow-summary-table td:nth-child(8){width:8%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(9),
#viewOptionsWindow .cashflow-summary-table td:nth-child(9){width:8%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(10),
#viewOptionsWindow .cashflow-summary-table td:nth-child(10){width:8%}
#viewOptionsWindow .cashflow-summary-table th:nth-child(11),
#viewOptionsWindow .cashflow-summary-table td:nth-child(11){width:18%}

#viewOptionsWindow .card{
  margin:8px 0!important;
}

@media(max-width:1100px){
  #viewOptionsWindow .cashflow-summary-table{font-size:9.5px!important}
  #viewOptionsWindow .cashflow-summary-table th,
  #viewOptionsWindow .cashflow-summary-table td{
    padding:5px 2px!important;
    font-size:9.5px!important;
  }
}

/* V45 - tighter, centered View Options table */
#viewOptionsWindow .cashflow-summary-table{
  width:100%!important;
  min-width:0!important;
  table-layout:fixed!important;
  font-size:10px!important;
}

#viewOptionsWindow .cashflow-summary-table th,
#viewOptionsWindow .cashflow-summary-table td{
  text-align:center!important;
  vertical-align:middle!important;
}

#viewOptionsWindow .cashflow-summary-table th{
  padding:5px 2px!important;
  line-height:1.05!important;
  white-space:normal!important;
  font-size:9.5px!important;
}

#viewOptionsWindow .cashflow-summary-table td{
  padding:5px 2px!important;
  font-size:9.5px!important;
  white-space:nowrap!important;
}

/* Tighter daily table column widths */
#viewOptionsWindow .cashflow-summary-table th:nth-child(1),
#viewOptionsWindow .cashflow-summary-table td:nth-child(1){width:9%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(2),
#viewOptionsWindow .cashflow-summary-table td:nth-child(2){width:6%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(3),
#viewOptionsWindow .cashflow-summary-table td:nth-child(3){width:8%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(4),
#viewOptionsWindow .cashflow-summary-table td:nth-child(4){width:8%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(5),
#viewOptionsWindow .cashflow-summary-table td:nth-child(5){width:8%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(6),
#viewOptionsWindow .cashflow-summary-table td:nth-child(6){width:6%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(7),
#viewOptionsWindow .cashflow-summary-table td:nth-child(7){width:6%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(8),
#viewOptionsWindow .cashflow-summary-table td:nth-child(8){width:7%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(9),
#viewOptionsWindow .cashflow-summary-table td:nth-child(9){width:7%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(10),
#viewOptionsWindow .cashflow-summary-table td:nth-child(10){width:7%!important}
#viewOptionsWindow .cashflow-summary-table th:nth-child(11),
#viewOptionsWindow .cashflow-summary-table td:nth-child(11){width:12%!important}

/* Center the summary heading row too */
#viewOptionsWindow .summary-table-card > div:first-child{
  align-items:center!important;
}

/* Make top summary cards slightly tighter */
#viewOptionsWindow .view-summary{
  text-align:center!important;
  padding:10px 12px!important;
}
#viewOptionsWindow .view-summary b{
  display:block!important;
  text-align:center!important;
}
#viewOptionsWindow .view-summary .amt{
  text-align:center!important;
  font-size:22px!important;
}

/* Keep popup nearly full-screen */
#viewOptionsWindow .upload-window-box,
#viewOptionsWindow .view-window-box{
  width:99.5vw!important;
  max-width:1600px!important;
  padding:14px!important;
}

.money-forecast-card{
  border:2px solid #8b5cf6!important;
  background:#f5f3ff!important;
}
.money-forecast-card:hover{
  transform:translateY(-2px);
  box-shadow:0 8px 22px rgba(139,92,246,.16);
}

.forecast-window-box{
  width:min(1450px,98vw)!important;
  max-width:1450px!important;
  max-height:96vh!important;
  overflow:auto!important;
}

.forecast-toolbar{
  display:grid;
  grid-template-columns:repeat(3,minmax(180px,1fr));
  gap:12px;
}

.forecast-toolbar label,
.forecast-input-grid label{
  margin:0;
}

.forecast-kpi-grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:10px;
  margin:12px 0;
}

.forecast-kpi{
  border-radius:14px;
  padding:14px 16px;
  border:1px solid #e2e8f0;
  background:#fff;
}

.forecast-kpi span{
  display:block;
  font-size:12px;
  color:#64748b;
  margin-bottom:6px;
}

.forecast-kpi b{
  font-size:24px;
}

.forecast-kpi.current{background:#f8fafc}
.forecast-kpi.freecash{background:#eff6ff}
.forecast-kpi.safe{background:#f0fdf4}
.forecast-kpi.end{background:#fff7ed}

.forecast-decision{
  display:flex;
  flex-direction:column;
  gap:5px;
  padding:14px 16px;
  border-radius:12px;
  margin:10px 0 14px;
  border:1px solid;
}
.forecast-decision.good{background:#f0fdf4;border-color:#86efac;color:#166534}
.forecast-decision.warn{background:#fffbeb;border-color:#fde68a;color:#92400e}
.forecast-decision.bad{background:#fef2f2;border-color:#fecaca;color:#991b1b}
.forecast-decision b{font-size:16px}
.forecast-decision span{font-size:13px}

.forecast-columns{
  display:grid;
  grid-template-columns:1.2fr .8fr;
  gap:12px;
}

.forecast-input-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:10px;
}

.forecast-formula-table,
.forecast-history-table{
  width:100%;
  border-collapse:collapse;
}

.forecast-formula-table td,
.forecast-history-table th,
.forecast-history-table td{
  padding:8px;
  border-bottom:1px solid #e5e7eb;
}

.forecast-formula-table td:last-child,
.forecast-history-table td:not(:first-child){
  text-align:right;
}

.forecast-history-table th{
  background:#f8fafc;
}

@media(max-width:900px){
  .forecast-kpi-grid{grid-template-columns:1fr 1fr}
  .forecast-columns{grid-template-columns:1fr}
  .forecast-toolbar{grid-template-columns:1fr}
}
@media(max-width:600px){
  .forecast-kpi-grid{grid-template-columns:1fr}
  .forecast-input-grid{grid-template-columns:1fr}
}

/* V47 — redesigned View Options */
#viewOptionsWindow .view-mode-square-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(190px,220px))!important;
  justify-content:center!important;
  gap:18px!important;
  margin:22px auto!important;
}

#viewOptionsWindow .view-mode-square{
  width:220px!important;
  height:205px!important;
  padding:20px!important;
  border-radius:18px!important;
  display:flex!important;
  flex-direction:column!important;
  align-items:center!important;
  justify-content:center!important;
  text-align:center!important;
  gap:9px!important;
}

#viewOptionsWindow .view-mode-square .upload-choice-icon{
  font-size:38px!important;
}

#viewOptionsWindow .view-mode-square b{
  font-size:18px!important;
}

#viewOptionsWindow .view-mode-square span{
  font-size:12px!important;
  line-height:1.35!important;
  color:#64748b!important;
}

.view-section-title{
  margin:10px 0 6px;
}
.view-section-title h2{
  margin:0 0 4px;
}
.compact-period-control{
  display:flex;
  align-items:end;
  gap:10px;
  flex-wrap:wrap;
  padding:10px 14px!important;
  margin:8px 0!important;
}
.compact-period-control label{
  margin:0!important;
}
.compact-period-control input{
  margin-top:4px!important;
}

.overall-report-heading{
  display:flex;
  justify-content:space-between;
  gap:12px;
  align-items:center;
  flex-wrap:wrap;
  background:#fff;
  border-radius:12px;
  padding:12px 14px;
  margin:8px 0;
}
.overall-report-heading h3{
  margin:0 0 2px;
}

.overall-main-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(145px,1fr));
  gap:9px;
  margin:9px 0 12px;
}
.overall-main-total{
  padding:12px;
  border-radius:13px;
  border:1px solid #dbe3ec;
  display:flex;
  flex-direction:column;
  text-align:center;
  gap:4px;
}
.overall-main-total strong{
  font-size:19px;
}
.overall-main-total span{
  font-size:11px;
  color:#64748b;
}

.overall-detail-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(250px,1fr));
  gap:10px;
}
.overall-category-card{
  background:#fff;
  border-radius:13px;
  border:1px solid #e2e8f0;
  padding:10px;
}
.overall-category-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  padding:7px 9px;
  border-radius:9px;
  margin-bottom:5px;
}
.overall-category-head h3{
  margin:0;
  font-size:15px;
}
.overall-sub-table{
  width:100%;
  border-collapse:collapse;
  font-size:11px;
}
.overall-sub-table th,
.overall-sub-table td{
  padding:6px 5px;
  border-bottom:1px solid #e5e7eb;
  text-align:center;
}
.overall-sub-table td:first-child,
.overall-sub-table th:first-child{
  text-align:left;
}

.tone-green{background:#ecfdf5!important;border-color:#86efac!important}
.tone-red{background:#fef2f2!important;border-color:#fca5a5!important}
.tone-blue{background:#eff6ff!important;border-color:#93c5fd!important}
.tone-cyan{background:#ecfeff!important;border-color:#67e8f9!important}
.tone-orange{background:#fff7ed!important;border-color:#fdba74!important}
.tone-grey{background:#f8fafc!important;border-color:#cbd5e1!important}

.category-analysis-tabs{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
  gap:8px;
  margin:10px 0;
}
.category-analysis-tab{
  min-height:92px;
  border-radius:13px;
  border:1px solid #cbd5e1;
  background:#fff;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:3px;
  padding:8px;
}
.category-analysis-tab b{font-size:14px}
.category-analysis-tab span{font-size:13px;font-weight:800}
.category-analysis-tab small{font-size:10px;color:#64748b}
.category-analysis-tab.active{
  background:#2563eb;
  color:#fff;
  border-color:#2563eb;
}
.category-analysis-tab.active small{color:#dbeafe}

.category-analysis-summary{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:8px;
  padding:12px;
  border-radius:13px;
  margin:8px 0;
}
.category-analysis-summary div{
  text-align:center;
}
.category-analysis-summary span{
  display:block;
  font-size:11px;
  color:#64748b;
}
.category-analysis-summary b{
  font-size:19px;
}
.category-analysis-grid{
  display:grid;
  grid-template-columns:.8fr 1.2fr;
  gap:10px;
}
.category-analysis-scroll{
  max-height:430px;
  overflow:auto;
}

@media(max-width:900px){
  #viewOptionsWindow .view-mode-square-grid{
    grid-template-columns:repeat(2,minmax(180px,220px))!important;
  }
  .overall-detail-grid{grid-template-columns:1fr 1fr}
  .category-analysis-grid{grid-template-columns:1fr}
}
@media(max-width:600px){
  #viewOptionsWindow .view-mode-square-grid{
    grid-template-columns:1fr!important;
  }
  #viewOptionsWindow .view-mode-square{
    width:100%!important;
    height:auto!important;
    min-height:170px!important;
  }
  .overall-detail-grid{grid-template-columns:1fr}
  .category-analysis-summary{grid-template-columns:1fr}
}

/* V48 fix: when a report is opened, hide the 3 option cards completely */
#viewOptionsWindow #viewModeChooser[style*="display: none"],
#viewOptionsWindow #viewModeChooser[style*="display:none"]{
  display:none!important;
}

/* Keep the opened report at the top instead of leaving a large blank area */
#viewOptionsWindow #viewModeContent{
  margin-top:6px!important;
}

/* V50 Option 3 - Google Sheet style period summary */
.option3-summary-card{
  padding:12px!important;
  margin-top:10px!important;
}
.option3-summary-card h3{
  margin:0 0 10px!important;
}
.option3-period-table-wrap{
  overflow:auto;
}
.option3-period-table{
  width:100%;
  border-collapse:collapse;
  table-layout:fixed;
  font-size:11px;
  background:#fff;
}
.option3-period-table th{
  background:#3b82f6;
  color:#fff;
  padding:7px 5px;
  border:1px solid #cbd5e1;
  text-align:center;
  white-space:normal;
  line-height:1.1;
}
.option3-period-table td{
  padding:6px 5px;
  border:1px solid #e2e8f0;
  text-align:center;
  white-space:nowrap;
}
.option3-period-table th:nth-child(1),
.option3-period-table td:nth-child(1){width:15%}
.option3-period-table th:nth-child(2),
.option3-period-table td:nth-child(2){width:12%}
.option3-period-table th:nth-child(3),
.option3-period-table td:nth-child(3){width:14%}
.option3-period-table th:nth-child(4),
.option3-period-table td:nth-child(4){width:14%}
.option3-period-table th:nth-child(5),
.option3-period-table td:nth-child(5){width:14%}
.option3-period-table th:nth-child(6),
.option3-period-table td:nth-child(6){width:14%}
.option3-period-table th:nth-child(7),
.option3-period-table td:nth-child(7){width:17%}

/* Monthly / Yearly have no Day column, so allow natural redistribution */
@media(max-width:800px){
  .option3-period-table{font-size:10px}
  .option3-period-table th,
  .option3-period-table td{padding:5px 3px}
}

.option3-total-grid{
  display:grid;
  grid-template-columns:repeat(5,minmax(135px,1fr));
  gap:8px;
  margin:0 0 12px;
}
.option3-total{
  border:2px solid #cbd5e1;
  border-radius:12px;
  padding:10px 12px;
  min-height:68px;
  display:flex;
  flex-direction:column;
  justify-content:center;
}
.option3-total span{
  font-size:12px;
  font-weight:700;
  margin-bottom:4px;
}
.option3-total b{
  font-size:20px;
  line-height:1.15;
  white-space:nowrap;
}
.option3-total.income-total{background:#ecfdf5;border-color:#22c55e;color:#08783d}
.option3-total.expense-total{background:#fff1f2;border-color:#ef4444;color:#dc2626}
.option3-total.saving-total{background:#eff6ff;border-color:#3b82f6;color:#2563eb}
.option3-total.others-total{background:#f8fafc;border-color:#94a3b8;color:#334155}
.option3-total.balance-total{background:#f0fdf4;border-color:#16a34a;color:#166534}
@media(max-width:900px){
  .option3-total-grid{grid-template-columns:repeat(3,1fr)}
}

/* V52 - Option 1 overall summary + transaction pass-through table */
.option1-overall-summary{
  max-width:760px;
  margin:10px 0 12px!important;
  padding:14px 18px!important;
}
.option1-overall-summary h3{
  margin:0 0 10px;
}
.option1-summary-table{
  width:100%;
  border-collapse:collapse;
  font-size:14px;
}
.option1-summary-table th{
  background:#bbf7d0;
  padding:9px 10px;
  text-align:center;
}
.option1-summary-table td{
  padding:9px 10px;
  border-bottom:1px solid #e2e8f0;
}
.option1-summary-table td:nth-child(2),
.option1-summary-table td:nth-child(3){
  text-align:right;
}
.option1-remaining-row td{
  font-size:15px;
  border-top:2px solid #cbd5e1;
}

.option1-transaction-card{
  margin-top:12px!important;
}
.option1-transaction-card h3{
  margin:0 0 10px!important;
}
.option1-transaction-wrap{
  overflow:auto;
  max-height:480px;
  border:1px solid #e2e8f0;
  border-radius:10px;
}
.option1-transaction-table{
  width:100%;
  min-width:860px;
  border-collapse:collapse;
  font-size:11px;
}
.option1-transaction-table th{
  position:sticky;
  top:0;
  z-index:2;
  background:#3b82f6;
  color:#fff;
  padding:7px 6px;
  text-align:center;
}
.option1-transaction-table td{
  padding:7px 6px;
  border-bottom:1px solid #e5e7eb;
}
.option1-transaction-table td:nth-child(5){
  text-align:right;
  font-weight:700;
}

/* V55 - Option 1 click-through transactions */
.option1-clickable-card{
  cursor:pointer!important;
  width:100%;
  font:inherit;
}
.option1-clickable-card:hover{
  transform:translateY(-2px);
  box-shadow:0 7px 18px rgba(15,23,42,.12);
}
.option1-sub-click-row{
  cursor:pointer;
}
.option1-sub-click-row:hover td{
  background:rgba(59,130,246,.08);
}
.option1-sub-click-row td:first-child{
  text-decoration:underline;
  text-decoration-style:dotted;
  text-underline-offset:3px;
}

.option1-popup-box{
  width:min(1350px,98vw)!important;
  max-width:1350px!important;
  max-height:94vh!important;
}
.option1-popup-filter{
  margin:10px 0;
}
.option1-popup-filter input{
  width:100%;
  margin:0;
}
.option1-popup-table-wrap{
  max-height:70vh;
  overflow:auto;
  border:1px solid #e2e8f0;
  border-radius:10px;
}
.option1-popup-table{
  width:100%;
  min-width:980px;
  border-collapse:collapse;
  background:#fff;
  font-size:11px;
}
.option1-popup-table th{
  position:sticky;
  top:0;
  z-index:2;
  background:#3b82f6;
  color:#fff;
  padding:8px 6px;
  text-align:center;
}
.option1-popup-table td{
  padding:7px 6px;
  border-bottom:1px solid #e5e7eb;
  text-align:center;
}
.option1-popup-table td:nth-child(5){
  text-align:left;
  max-width:280px;
}
.option1-popup-amount{
  font-weight:800;
  text-align:right!important;
}

/* V56 - Attractive My Tracking opening screen */
.welcome{background:radial-gradient(circle at 15% 20%,rgba(37,99,235,.13),transparent 30%),radial-gradient(circle at 85% 25%,rgba(34,197,94,.12),transparent 30%),radial-gradient(circle at 70% 85%,rgba(168,85,247,.10),transparent 35%),linear-gradient(135deg,#f8fbff,#eefbf6)!important;padding:28px!important}
.modern-welcome-card{width:min(1050px,96vw)!important;padding:34px!important;border-radius:28px!important;text-align:left!important;background:rgba(255,255,255,.95)!important;backdrop-filter:blur(12px);box-shadow:0 24px 70px rgba(15,23,42,.15)!important;border:1px solid rgba(148,163,184,.18)}
.welcome-brand-row{display:flex;gap:18px;align-items:center;margin-bottom:24px}.welcome-logo{width:76px;height:76px;border-radius:22px;display:grid;place-items:center;font-size:42px;background:linear-gradient(135deg,#dcfce7,#dbeafe);box-shadow:0 10px 25px rgba(37,99,235,.12)}
.welcome-kicker{font-size:11px;font-weight:800;letter-spacing:1.5px;color:#2563eb;margin-bottom:4px}.modern-welcome-card h1{font-size:46px!important;margin:0!important;letter-spacing:-1px}.modern-welcome-card p{margin:7px 0 0!important;font-size:15px!important;color:#64748b!important}
.welcome-feature-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}.welcome-feature{border-radius:18px;padding:16px;min-height:150px;display:flex;flex-direction:column;gap:12px;border:1px solid #e2e8f0;transition:.2s ease}.welcome-feature:hover{transform:translateY(-3px);box-shadow:0 12px 24px rgba(15,23,42,.08)}
.welcome-feature.money{background:#ecfdf5;border-color:#86efac}.welcome-feature.health{background:#fff1f2;border-color:#fda4af}.welcome-feature.job{background:#fff7ed;border-color:#fdba74}.welcome-feature.productivity{background:#eff6ff;border-color:#93c5fd}.welcome-feature.efficiency{background:#faf5ff;border-color:#d8b4fe}.welcome-feature-icon{font-size:30px}.welcome-feature b{font-size:17px}.welcome-feature span{font-size:12px;line-height:1.4;color:#64748b}
.welcome-bottom{margin-top:22px;display:flex;justify-content:space-between;align-items:center;gap:20px;background:#0f172a;color:#fff;border-radius:18px;padding:18px 20px}.welcome-message{display:flex;flex-direction:column;gap:3px}.welcome-message b{font-size:17px}.welcome-message span{color:#cbd5e1;font-size:12px}.modern-start{margin:0!important;padding:13px 24px!important;border-radius:12px!important;background:linear-gradient(135deg,#2563eb,#7c3aed)!important;min-width:190px;white-space:nowrap}.job-home-grid{grid-template-columns:repeat(4,1fr)!important}
@media(max-width:950px){.welcome-feature-grid{grid-template-columns:repeat(2,1fr)}.job-home-grid{grid-template-columns:repeat(2,1fr)!important}}@media(max-width:600px){.modern-welcome-card{padding:22px!important}.welcome-brand-row{align-items:flex-start}.modern-welcome-card h1{font-size:36px!important}.welcome-feature-grid{grid-template-columns:1fr}.welcome-bottom{flex-direction:column;align-items:stretch}.modern-start{width:100%}.job-home-grid{grid-template-columns:1fr!important}}

/* V57 - Visual editorial landing page */
.visual-welcome{
  min-height:100vh!important;
  padding:24px!important;
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  background:
    radial-gradient(circle at 12% 18%,rgba(80,91,255,.25),transparent 28%),
    radial-gradient(circle at 86% 80%,rgba(255,108,125,.20),transparent 34%),
    linear-gradient(135deg,#eef3ff 0%,#f8f3ff 48%,#fff5ef 100%)!important;
  overflow:auto!important;
}
.visual-landing-shell{
  width:min(1180px,96vw);
  min-height:680px;
  display:grid;
  grid-template-columns:.9fr 1.1fr;
  background:#fff;
  border-radius:34px;
  overflow:hidden;
  box-shadow:0 30px 90px rgba(23,29,66,.18);
  border:1px solid rgba(255,255,255,.8);
}
.visual-copy-panel{
  position:relative;
  padding:70px 58px 54px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  background:
    linear-gradient(160deg,rgba(255,255,255,.98),rgba(248,249,255,.96));
}
.visual-copy-panel:after{
  content:"";
  position:absolute;
  right:-70px;
  bottom:-100px;
  width:260px;
  height:260px;
  border-radius:50%;
  background:linear-gradient(135deg,#7c3aed22,#2563eb10);
  filter:blur(2px);
}
.visual-eyebrow{
  display:inline-block;
  width:max-content;
  padding:7px 11px;
  border-radius:999px;
  background:#eef2ff;
  color:#4f46e5;
  font-size:11px;
  font-weight:900;
  letter-spacing:1.7px;
  margin-bottom:18px;
}
.visual-copy-panel h1{
  margin:0!important;
  font-size:68px!important;
  line-height:.98!important;
  letter-spacing:-3px!important;
  color:#101632!important;
}
.visual-lead{
  margin:20px 0 0!important;
  max-width:480px;
  font-size:20px!important;
  line-height:1.45!important;
  color:#4f5b78!important;
  font-weight:500;
}
.visual-quote{
  position:relative;
  margin:34px 0 28px;
  padding:20px 22px 20px 24px;
  border-left:4px solid #6d5dfc;
  border-radius:0 14px 14px 0;
  background:linear-gradient(90deg,#f1efff,#f9f9ff);
  color:#303a5b;
  font-size:17px;
  line-height:1.55;
  font-weight:700;
}
.visual-topics{
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  gap:9px;
  color:#626d88;
  font-size:11px;
  font-weight:900;
  letter-spacing:.8px;
  text-transform:uppercase;
}
.visual-topics i{
  display:block;
  width:4px;
  height:4px;
  border-radius:50%;
  background:#9ca6bd;
}
.visual-actions{
  margin-top:38px;
  display:flex;
  align-items:center;
  gap:18px;
  flex-wrap:wrap;
}
.visual-start{
  border:0;
  border-radius:14px;
  padding:16px 30px;
  background:linear-gradient(135deg,#315cf5,#7c3aed);
  color:#fff;
  font-size:14px;
  font-weight:900;
  letter-spacing:.7px;
  box-shadow:0 12px 28px rgba(78,70,229,.28);
  cursor:pointer;
  transition:transform .2s ease,box-shadow .2s ease;
}
.visual-start:hover{
  transform:translateY(-2px);
  box-shadow:0 16px 32px rgba(78,70,229,.34);
}
.visual-hint{
  max-width:230px;
  color:#7a849b;
  font-size:11px;
  line-height:1.45;
}
.visual-art-panel{
  position:relative;
  min-height:680px;
  padding:20px;
  background:linear-gradient(155deg,#151a43,#34246f);
  overflow:hidden;
}
.tracking-hero-art{
  display:block;
  width:100%;
  height:100%;
  max-height:640px;
  min-height:620px;
  object-fit:cover;
  border-radius:24px;
}
.visual-art-panel:after{
  content:"";
  position:absolute;
  inset:auto -110px -160px auto;
  width:330px;
  height:330px;
  border-radius:50%;
  background:#ff8a782f;
  filter:blur(10px);
  pointer-events:none;
}
.visual-art-caption{
  position:absolute;
  right:42px;
  top:42px;
  z-index:3;
  display:flex;
  flex-direction:column;
  align-items:flex-end;
  gap:4px;
  color:#fff;
}
.visual-art-caption span{
  font-size:10px;
  font-weight:900;
  letter-spacing:2px;
  color:#d7dcff;
}
.visual-art-caption b{
  font-size:14px;
}
@media(max-width:900px){
  .visual-landing-shell{grid-template-columns:1fr;min-height:auto}
  .visual-copy-panel{padding:50px 34px}
  .visual-copy-panel h1{font-size:54px!important}
  .visual-art-panel{min-height:480px}
  .tracking-hero-art{min-height:440px;max-height:480px}
}
@media(max-width:560px){
  .visual-welcome{padding:10px!important}
  .visual-landing-shell{border-radius:22px}
  .visual-copy-panel{padding:38px 24px}
  .visual-copy-panel h1{font-size:45px!important;letter-spacing:-2px!important}
  .visual-lead{font-size:17px!important}
  .visual-quote{font-size:15px;margin:25px 0 20px}
  .visual-art-panel{padding:12px;min-height:390px}
  .tracking-hero-art{min-height:365px}
  .visual-art-caption{right:28px;top:28px}
}


/* V58 - richer colourful landing */
.visual-welcome{
  background:
    radial-gradient(circle at 8% 14%,rgba(255,0,128,.22),transparent 28%),
    radial-gradient(circle at 92% 12%,rgba(255,174,0,.22),transparent 28%),
    radial-gradient(circle at 18% 88%,rgba(0,207,255,.20),transparent 30%),
    linear-gradient(135deg,#130b2f 0%,#2b145c 42%,#4a1649 72%,#8a3a19 100%)!important;
}
.visual-landing-shell{
  width:min(1240px,97vw)!important;
  min-height:700px!important;
  grid-template-columns:.88fr 1.12fr!important;
  border-radius:30px!important;
  background:linear-gradient(145deg,rgba(18,12,45,.97),rgba(35,16,66,.97))!important;
  border:1px solid rgba(255,255,255,.18)!important;
  box-shadow:0 36px 100px rgba(0,0,0,.38)!important;
}
.visual-copy-panel{
  padding:66px 54px 50px!important;
  color:white!important;
  background:
    radial-gradient(circle at 10% 15%,rgba(255,0,153,.18),transparent 28%),
    radial-gradient(circle at 90% 82%,rgba(255,174,0,.12),transparent 35%),
    linear-gradient(160deg,#130d31 0%,#241447 55%,#311445 100%)!important;
}
.visual-eyebrow{
  color:#ffe0f0!important;
  background:linear-gradient(90deg,#ff2f92,#7c3aed)!important;
  box-shadow:0 7px 18px rgba(255,47,146,.25);
}
.visual-copy-panel h1{
  color:#fff!important;
  font-size:72px!important;
  background:linear-gradient(90deg,#ffffff 0%,#ffcf4a 48%,#ff5fa2 100%);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}
.visual-lead{color:#f1e8ff!important;font-size:21px!important}
.visual-quote{
  color:#fff!important;
  border-left-color:#ffcf4a!important;
  background:linear-gradient(90deg,rgba(255,95,162,.16),rgba(124,58,237,.12))!important;
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.07);
}
.visual-topics{color:#ffd8ef!important;gap:10px!important}
.visual-topics i{background:#ffcf4a!important}
.visual-start{
  padding:17px 34px!important;
  font-size:15px!important;
  background:linear-gradient(90deg,#ff168a,#ff7a2f,#ffc21a)!important;
  box-shadow:0 14px 34px rgba(255,82,94,.35)!important;
}
.visual-hint{color:#cfc7e8!important}
.saree-hero-panel{
  position:relative;
  min-height:700px!important;
  padding:0!important;
  overflow:hidden;
  background:#1a1030!important;
}
.tracking-hero-photo{
  object-position:center center;
  width:100%;height:100%;min-height:700px;display:block;object-fit:cover;object-position:center 25%;
  filter:saturate(1.08) contrast(1.04);
}
.saree-hero-panel:before{
  content:"";position:absolute;inset:0;z-index:1;
  background:linear-gradient(90deg,rgba(20,10,45,.30),transparent 32%,transparent 70%,rgba(20,10,45,.08));
}
.hero-glow{position:absolute;border-radius:50%;filter:blur(28px);z-index:2;pointer-events:none}
.hero-glow-one{width:190px;height:190px;right:-30px;top:40px;background:rgba(255,183,58,.30)}
.hero-glow-two{width:220px;height:220px;left:-60px;bottom:-40px;background:rgba(255,34,133,.22)}
.visual-art-caption{z-index:3!important;background:rgba(20,12,46,.50);backdrop-filter:blur(8px);padding:10px 14px;border-radius:12px;border:1px solid rgba(255,255,255,.14)}
.hero-quote-chip{
  position:absolute;z-index:3;left:28px;bottom:28px;max-width:330px;
  color:#fff;font-weight:800;font-size:14px;line-height:1.35;
  padding:14px 16px;border-radius:16px;
  background:linear-gradient(135deg,rgba(255,31,130,.82),rgba(124,58,237,.76));
  box-shadow:0 12px 30px rgba(0,0,0,.22);
}
@media(max-width:900px){
  .visual-landing-shell{grid-template-columns:1fr!important}
  .saree-hero-panel,.tracking-hero-photo{min-height:470px!important}
  .visual-copy-panel h1{font-size:56px!important}
}
@media(max-width:560px){
  .visual-copy-panel h1{font-size:46px!important}
  .saree-hero-panel,.tracking-hero-photo{min-height:390px!important}
}


/* V59 - Finance dashboard inspired Money UI */
.money-dashboard-shell{max-width:1240px!important}
.money-dashboard-head{
  display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:16px
}
.money-dashboard-head h1{margin:2px 0 4px;font-size:34px}
.money-eyebrow{font-size:11px;font-weight:800;letter-spacing:1.4px;color:#15803d}
.money-head-actions{display:flex;gap:8px}

.money-hero-card{
  background:linear-gradient(135deg,#0f2f24,#164e3b);
  border-radius:22px;padding:22px;color:#fff;display:grid;
  grid-template-columns:1.1fr 1.9fr;gap:18px;margin-bottom:14px;
  box-shadow:0 16px 34px rgba(22,78,59,.18)
}
.money-balance-block{display:flex;flex-direction:column;justify-content:center}
.money-balance-block span{font-size:13px;color:#bbf7d0}
.money-balance-block strong{font-size:40px;margin:8px 0}
.money-balance-block small{font-size:11px;color:#a7f3d0;line-height:1.45}
.money-hero-mini-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.money-mini-stat{
  border:1px solid rgba(255,255,255,.16);border-radius:16px;padding:14px;text-align:left;
  background:rgba(255,255,255,.08);color:#fff;display:flex;flex-direction:column;gap:5px
}
.money-mini-stat:hover{background:rgba(255,255,255,.13)}
.money-mini-stat span{font-size:12px}
.money-mini-stat b{font-size:20px}
.money-mini-stat small{font-size:10px;color:#d1fae5}
.money-mini-stat.expense small,.money-mini-stat.saving small{color:#e2e8f0}

.money-chart-grid{display:grid;grid-template-columns:1.55fr .85fr;gap:14px;margin-bottom:14px}
.money-lower-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.money-chart-card{
  background:#fff;border:1px solid #e5e7eb;border-radius:18px;padding:16px;
  box-shadow:0 8px 22px rgba(15,23,42,.055)
}
.money-card-title-row{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:10px}
.money-card-title-row h3{margin:0;font-size:17px}
.money-card-title-row p{margin:3px 0 0;color:#64748b;font-size:11px}
.money-legend{display:flex;gap:12px;font-size:10px;color:#64748b}
.money-legend span{display:flex;align-items:center;gap:5px}
.money-legend i{width:8px;height:8px;border-radius:50%;display:inline-block}
.legend-income{background:#16a34a}.legend-expense{background:#f97373}

.money-svg-chart{height:260px;width:100%}
.money-svg-chart svg{width:100%;height:100%}
.money-empty-chart{height:220px;display:grid;place-items:center;color:#94a3b8}

.money-donut-layout{display:grid;grid-template-columns:170px 1fr;gap:14px;align-items:center}
.money-donut{
  width:165px;height:165px;border-radius:50%;position:relative;display:grid;place-items:center
}
.money-donut:after{
  content:"";position:absolute;width:105px;height:105px;border-radius:50%;background:#fff
}
.money-donut-center{position:relative;z-index:1;text-align:center;display:flex;flex-direction:column;gap:3px}
.money-donut-center small{font-size:10px;color:#64748b}
.money-donut-center b{font-size:14px}
.money-breakdown-list{display:flex;flex-direction:column;gap:8px}
.money-breakdown-row{display:flex;justify-content:space-between;gap:8px;align-items:center;font-size:11px}
.money-breakdown-name{display:flex;gap:6px;align-items:center}
.money-breakdown-name i{width:8px;height:8px;border-radius:50%}
.money-breakdown-row>span:last-child{text-align:right}
.money-breakdown-row small{display:block;color:#94a3b8;font-size:9px}

.money-progress-list{display:flex;flex-direction:column;gap:13px}
.money-progress-top{display:flex;justify-content:space-between;font-size:11px;margin-bottom:5px}
.money-progress-track{height:8px;border-radius:999px;background:#eef2f7;overflow:hidden}
.money-progress-track span{display:block;height:100%;border-radius:999px}

.money-movement-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}
.movement-stat{
  border:1px solid #e2e8f0;background:#f8fafc;border-radius:14px;padding:12px;text-align:left;
  display:flex;flex-direction:column;gap:4px
}
.movement-stat span{font-size:10px;color:#64748b}
.movement-stat b{font-size:17px}
.movement-stat small{font-size:9px;color:#94a3b8}

.money-recent-card{margin-bottom:12px}
.money-recent-table{display:flex;flex-direction:column}
.money-recent-row{
  display:flex;justify-content:space-between;align-items:center;gap:12px;
  padding:10px 2px;border-bottom:1px solid #eef2f7
}
.money-recent-row:last-child{border-bottom:0}
.money-recent-row div{display:flex;flex-direction:column;gap:2px}
.money-recent-row b{font-size:12px}
.money-recent-row span{font-size:10px;color:#94a3b8}
.money-recent-row strong{font-size:12px}
.money-recent-row .positive{color:#15803d}.money-recent-row .negative{color:#dc2626}

.money-quick-actions{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:12px 0}
.money-quick-actions button{
  border-radius:12px;padding:10px 8px;background:#fff;border:1px solid #dbe3ea;font-weight:700;color:#334155
}
.money-quick-actions button:hover{border-color:#22c55e;background:#f0fdf4}

.money-sync-compact{margin-top:10px!important;padding:14px!important}

@media(max-width:950px){
  .money-hero-card{grid-template-columns:1fr}
  .money-chart-grid,.money-lower-grid{grid-template-columns:1fr}
}
@media(max-width:700px){
  .money-dashboard-head{align-items:flex-start;flex-direction:column}
  .money-hero-mini-grid{grid-template-columns:1fr}
  .money-donut-layout{grid-template-columns:1fr;justify-items:center}
  .money-quick-actions{grid-template-columns:repeat(2,1fr)}
}

/* V60 START button fix */
#welcome.force-hidden{display:none!important}
#app.force-visible{display:block!important}

/* V61 - familiar Money cards first, visuals second */
.money-original-grid{margin-bottom:24px!important}
.money-insights-heading{
  display:flex;justify-content:space-between;align-items:end;gap:14px;
  margin:28px 0 12px;padding-top:20px;border-top:1px solid #e2e8f0
}
.money-insights-heading h2{margin:3px 0 4px;font-size:24px}
.money-original-grid .tile{min-height:190px}
@media(max-width:700px){.money-original-grid .tile{min-height:auto}}

/* V64 - All-category analytics */
.money-all-category-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:14px;
  margin-bottom:14px;
}
.money-all-category-chart{
  display:flex;
  flex-direction:column;
  gap:11px;
  margin-top:6px;
}
.money-cat-row{
  display:grid;
  grid-template-columns:105px 1fr 130px;
  align-items:center;
  gap:10px;
}
.money-cat-label{
  font-size:11px;
  font-weight:800;
  color:#334155;
}
.money-cat-track{
  height:13px;
  background:#eef2f7;
  border-radius:999px;
  overflow:hidden;
}
.money-cat-track span{
  display:block;
  height:100%;
  min-width:2px;
  border-radius:999px;
}
.money-cat-value{
  text-align:right;
  font-size:11px;
  font-weight:800;
  white-space:nowrap;
}
.money-high-low-summary{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:10px;
  margin-top:16px;
}
.money-high-low-card{
  border-radius:14px;
  padding:12px;
  border:1px solid #e2e8f0;
  background:#f8fafc;
}
.money-high-low-card.high{background:#f0fdf4;border-color:#86efac}
.money-high-low-card.low{background:#fff7ed;border-color:#fdba74}
.money-high-low-card span{
  display:block;
  color:#64748b;
  font-size:10px;
  margin-bottom:4px;
}
.money-high-low-card b{
  display:block;
  font-size:15px;
}
.money-high-low-card small{
  display:block;
  margin-top:3px;
  color:#64748b;
  font-size:10px;
}

.money-trend-tabs{
  display:flex;
  gap:6px;
  flex-wrap:wrap;
  margin:6px 0 10px;
}
.money-trend-tab{
  background:#eef2f7;
  color:#334155;
  padding:7px 10px;
  border-radius:999px;
  font-size:10px;
  font-weight:800;
  border:1px solid #dbe3ea;
}
.money-trend-tab.active{
  background:#0f172a;
  color:#fff;
  border-color:#0f172a;
}
.money-selected-category-summary{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:8px;
  margin:8px 0 6px;
}
.money-trend-stat{
  padding:10px;
  border-radius:12px;
  background:#f8fafc;
  border:1px solid #e2e8f0;
}
.money-trend-stat span{
  display:block;
  color:#64748b;
  font-size:9px;
}
.money-trend-stat b{
  display:block;
  font-size:13px;
  margin-top:3px;
}
@media(max-width:950px){
  .money-all-category-grid{grid-template-columns:1fr}
}
@media(max-width:600px){
  .money-cat-row{grid-template-columns:80px 1fr 95px}
  .money-selected-category-summary{grid-template-columns:1fr}
}


.money-sub-trend-tabs{
  display:flex;
  gap:6px;
  flex-wrap:wrap;
  margin:0 0 10px;
  padding-top:2px;
}
.money-sub-trend-tab{
  background:#fff;
  color:#475569;
  padding:6px 9px;
  border-radius:9px;
  font-size:9.5px;
  font-weight:700;
  border:1px solid #cbd5e1;
}
.money-sub-trend-tab:hover{border-color:#60a5fa;background:#f8fbff}
.money-sub-trend-tab.active{
  background:#2563eb;
  color:#fff;
  border-color:#2563eb;
}


.money-subcategory-summary-table td:not(:first-child),
.money-subcategory-summary-table th:not(:first-child){
  text-align:right;
}


.money-overall-sub-bars{
  display:flex;
  flex-direction:column;
  gap:10px;
  margin-top:8px;
}
.money-overall-sub-row{
  display:grid;
  grid-template-columns:180px 1fr 130px;
  gap:10px;
  align-items:center;
}
.money-overall-sub-name{
  font-size:11px;
  font-weight:700;
  color:#334155;
}
.money-overall-sub-track{
  height:12px;
  background:#eef2f7;
  border-radius:999px;
  overflow:hidden;
}
.money-overall-sub-track span{
  display:block;
  height:100%;
  border-radius:999px;
}
.money-overall-sub-value{
  text-align:right;
  font-size:11px;
  font-weight:800;
  white-space:nowrap;
}
@media(max-width:700px){
  .money-overall-sub-row{
    grid-template-columns:120px 1fr 95px;
  }
}


/* V69 - Clean Overall Sub Category Overview */
.money-subcategory-overview-card{
  margin-bottom:14px;
  padding:18px!important;
}
.money-overall-badge{
  display:inline-block;
  margin-left:6px;
  padding:3px 8px;
  border-radius:999px;
  background:#eef2ff;
  color:#4f46e5;
  font-size:10px;
  vertical-align:middle;
}
.money-sub-info-note{
  margin:8px 0 12px;
  padding:9px 11px;
  border:1px solid #bfdbfe;
  background:#eff6ff;
  color:#1d4ed8;
  border-radius:9px;
  font-size:10.5px;
}
.money-filter-title{
  font-size:10.5px;
  font-weight:800;
  color:#334155;
  margin-bottom:7px;
}
.money-category-checks{
  display:flex;
  flex-wrap:wrap;
  gap:7px;
  margin-bottom:13px;
}
.money-category-check{
  display:flex;
  align-items:center;
  gap:6px;
  padding:7px 10px;
  border:1px solid #dbe3ea;
  border-radius:9px;
  background:#fff;
  cursor:pointer;
  user-select:none;
  font-size:10.5px;
  font-weight:800;
}
.money-category-check input{
  width:14px;
  height:14px;
  margin:0;
  accent-color:#2563eb;
}
.money-category-check .dot{
  width:8px;
  height:8px;
  border-radius:3px;
  display:inline-block;
}
.money-sub-table-head{
  display:grid;
  grid-template-columns:210px minmax(300px,1fr) 100px;
  gap:10px;
  padding:7px 8px;
  color:#64748b;
  font-size:10px;
  font-weight:800;
  border-bottom:1px solid #e2e8f0;
}
.money-sub-table-head span:nth-child(2){text-align:center}
.money-sub-table-head span:nth-child(3){text-align:right}
.money-overall-sub-bars{
  display:flex;
  flex-direction:column;
}
.money-overall-sub-row{
  display:grid;
  grid-template-columns:210px minmax(300px,1fr) 100px;
  gap:10px;
  align-items:center;
  padding:7px 8px;
  border-bottom:1px solid #f1f5f9;
}
.money-overall-sub-label{
  display:flex;
  align-items:center;
  gap:8px;
  min-width:0;
}
.money-overall-sub-label .dot{
  width:9px;
  height:9px;
  border-radius:50%;
  flex:0 0 auto;
}
.money-overall-sub-name{
  font-size:10.8px;
  font-weight:800;
  color:#1e293b;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.money-overall-sub-bar-area{
  display:grid;
  grid-template-columns:minmax(160px,1fr) 120px;
  gap:10px;
  align-items:center;
}
.money-overall-sub-track{
  height:11px;
  background:#f1f5f9;
  border-radius:999px;
  overflow:hidden;
}
.money-overall-sub-track span{
  display:block;
  height:100%;
  border-radius:999px;
}
.money-overall-sub-value{
  text-align:right;
  font-size:10.8px;
  font-weight:800;
  color:#0f172a;
  white-space:nowrap;
}
.money-overall-sub-share{
  text-align:right;
  font-size:10.5px;
  font-weight:700;
  color:#475569;
}
.money-sub-summary-cards{
  display:grid;
  grid-template-columns:repeat(6,minmax(120px,1fr));
  gap:8px;
  margin-top:14px;
}
.money-sub-summary-card{
  border:1px solid #e2e8f0;
  border-radius:12px;
  padding:10px;
  background:#f8fafc;
}
.money-sub-summary-card span{
  display:block;
  font-size:9.5px;
  color:#64748b;
  margin-bottom:3px;
}
.money-sub-summary-card b{
  display:block;
  font-size:14px;
  color:#0f172a;
}
.money-sub-summary-card small{
  display:block;
  margin-top:2px;
  font-size:9.5px;
  font-weight:800;
}
.money-sub-grand-total{
  margin-top:9px;
  padding:10px 12px;
  border-radius:10px;
  background:#eff6ff;
  border:1px solid #bfdbfe;
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  font-weight:800;
  color:#1d4ed8;
}
.money-sub-grand-total b{font-size:16px}
@media(max-width:1000px){
  .money-sub-summary-cards{grid-template-columns:repeat(3,1fr)}
}
@media(max-width:760px){
  .money-sub-table-head,
  .money-overall-sub-row{grid-template-columns:130px 1fr 70px}
  .money-overall-sub-bar-area{grid-template-columns:1fr 90px}
  .money-sub-summary-cards{grid-template-columns:repeat(2,1fr)}
}


.money-remaining-clickable{
  width:100%;
  text-align:left;
}
.money-remaining-clickable:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 24px rgba(22,101,52,.12);
}
.account-balance-modal-box{
  width:min(720px,96%);
}
.account-balance-total{
  margin:16px 0 12px;
  padding:15px 16px;
  border-radius:14px;
  background:#ecfdf5;
  border:1px solid #86efac;
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
}
.account-balance-total span{
  font-size:12px;
  color:#166534;
  font-weight:700;
}
.account-balance-total b{
  font-size:24px;
  color:#166534;
}
.account-balance-list{
  display:flex;
  flex-direction:column;
  gap:8px;
}
.account-balance-row{
  display:grid;
  grid-template-columns:1fr 150px 90px;
  align-items:center;
  gap:12px;
  padding:12px 14px;
  border:1px solid #e2e8f0;
  border-radius:12px;
  background:#fff;
}
.account-balance-name{
  font-weight:800;
  color:#1e293b;
}
.account-balance-value{
  text-align:right;
  font-weight:900;
  font-size:15px;
}
.account-balance-value.positive{color:#15803d}
.account-balance-value.negative{color:#dc2626}
.account-balance-share{
  text-align:right;
  color:#64748b;
  font-size:11px;
}
.account-balance-bar{
  grid-column:1 / -1;
  height:7px;
  background:#eef2f7;
  border-radius:999px;
  overflow:hidden;
}
.account-balance-bar span{
  display:block;
  height:100%;
  border-radius:999px;
}
.account-balance-note{
  margin-top:13px;
  padding:10px 12px;
  border-radius:10px;
  background:#f8fafc;
  color:#64748b;
  font-size:10.5px;
  line-height:1.45;
}
@media(max-width:600px){
  .account-balance-row{grid-template-columns:1fr 110px}
  .account-balance-share{display:none}
}


/* ============================================================
   V71 TIME BLOCKING PLANNER
   ============================================================ */
.time-planner-shell{max-width:1500px}
.time-page-head{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:14px}
.time-date-chip{padding:9px 14px;border-radius:999px;background:#fff7cc;border:1px solid #fde68a;font-weight:800;font-size:12px;color:#854d0e}
.tb-top-grid{display:grid;grid-template-columns:.9fr 1.6fr 1fr;gap:14px;margin-bottom:14px}
.tb-small-label{font-size:10px;font-weight:800;color:#64748b;letter-spacing:.08em}
.tb-big-number{font-size:30px;font-weight:900;margin:8px 0;color:#0f172a}
.tb-mini-row{display:flex;justify-content:space-between;gap:10px;color:#64748b;font-size:11px}
.tb-mini-row b{color:#0f172a}
.tb-focus-card{background:linear-gradient(135deg,#fffdf2,#f8fbff)}
.tb-focus-head{display:flex;justify-content:space-between;align-items:center;gap:12px}
.tb-timer-display{font-size:38px;font-weight:900;letter-spacing:.04em;margin-top:3px}
.tb-task-select{min-width:230px;max-width:48%;padding:9px 10px;border:1px solid #cbd5e1;border-radius:9px;background:#fff;font-weight:700}
.tb-timer-presets{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.tb-timer-presets>button,.tb-custom-minutes button{padding:7px 10px;border-radius:8px;background:#eef2f7;border:1px solid #dbe3ea;font-weight:800}
.tb-custom-minutes{display:flex;gap:4px}
.tb-custom-minutes input{width:65px;padding:7px;border:1px solid #cbd5e1;border-radius:8px}
.tb-timer-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
.tb-month-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin-top:10px}
.tb-month-stats div{background:#f8fafc;border:1px solid #e2e8f0;border-radius:11px;padding:10px;text-align:center}
.tb-month-stats b{display:block;font-size:20px}.tb-month-stats span{display:block;color:#64748b;font-size:9.5px;margin-top:2px}

.tb-work-grid{display:flex;flex-direction:column;gap:14px;align-items:stretch}
.tb-section-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:11px}
.tb-section-head h2{margin:0 0 3px;font-size:18px}
.tb-divider{height:1px;background:#e5e7eb;margin:15px 0}
.tb-priority-list{display:flex;flex-direction:column;gap:8px}
.tb-priority-item{display:grid;grid-template-columns:34px 1fr 80px;gap:9px;align-items:center;padding:10px 11px;border-radius:12px;border:1px solid #fde68a;background:#fffbeb}
.tb-priority-num{width:30px;height:30px;border-radius:9px;background:#f59e0b;color:#fff;display:grid;place-items:center;font-weight:900}
.tb-priority-item b{font-size:12px}.tb-priority-item span{font-size:10px;color:#64748b}
.tb-priority-time{text-align:right;font-weight:800!important;color:#92400e!important}

.tb-task-table-head,.tb-task-row{display:grid;grid-template-columns:42px minmax(170px,1fr) 90px 64px 105px 34px;gap:6px;align-items:center}
.tb-task-table-head{padding:7px 5px;color:#64748b;font-size:9.5px;font-weight:800;border-bottom:1px solid #e2e8f0}
.tb-task-row{padding:6px 5px;border-bottom:1px solid #f1f5f9}
.tb-task-row input,.tb-task-row select{width:100%;padding:7px 7px;border:1px solid #dbe3ea;border-radius:8px;background:#fff;font-size:10.5px}
.tb-task-row .tb-priority-input{text-align:center;font-weight:900}
.tb-delete-task{width:30px;height:30px;border-radius:8px;background:#fff1f2;color:#e11d48;border:1px solid #fecdd3;font-weight:900}
.tb-task-row.status-Done{background:#f0fdf4}
.tb-task-row.status-Hold{background:#fffbeb}
.tb-task-row.status-Moved{background:#f5f3ff}

.tb-day-plan-panel{width:100%;max-height:none;overflow:visible}
.tb-day-grid-head,.tb-hour-row{display:grid;grid-template-columns:72px repeat(3,1fr);gap:6px;align-items:stretch}
.tb-day-grid-head{position:sticky;top:0;z-index:3;background:#fff;padding:7px 0;color:#64748b;font-size:9.5px;font-weight:800;border-bottom:1px solid #e2e8f0}
.tb-24-grid{height:660px;overflow-y:auto;padding-right:3px}
.tb-hour-row{padding:4px 0;border-bottom:1px solid #f1f5f9}
.tb-hour-label{display:flex;align-items:center;justify-content:center;border-radius:8px;background:#f8fafc;font-size:10px;font-weight:900;color:#475569}
.tb-time-slot{min-height:40px;padding:6px;border-radius:8px;border:1px solid #e2e8f0;background:#fff;position:relative}
.tb-time-slot.past{opacity:.48;background:#f8fafc}
.tb-time-slot.current{border:2px solid #2563eb;background:#eff6ff}
.tb-slot-time{font-size:8.5px;color:#94a3b8;font-weight:800}
.tb-slot-select{width:100%;margin-top:3px;padding:4px 5px;border:0;background:transparent;font-size:9.5px;font-weight:700;color:#334155}
.tb-slot-select:focus{outline:1px solid #93c5fd;border-radius:5px}

.tb-status-cards{display:grid;grid-template-columns:repeat(5,1fr);gap:9px}
.tb-status-cards div{border-radius:12px;padding:11px;border:1px solid #e2e8f0;background:#f8fafc}
.tb-status-cards b{display:block;font-size:11px;margin-bottom:4px}
.tb-status-cards span{display:block;color:#64748b;font-size:9.5px;line-height:1.4}
.tb-history-table{width:100%;border-collapse:collapse;font-size:10.5px}
.tb-history-table th{padding:8px;text-align:left;background:#f1f5f9;color:#475569;border-bottom:1px solid #cbd5e1}
.tb-history-table td{padding:8px;border-bottom:1px solid #e5e7eb}
.tb-history-table td:nth-child(n+3),.tb-history-table th:nth-child(n+3){text-align:right}
.tb-empty{padding:20px;text-align:center;color:#94a3b8;font-size:11px}

@media(max-width:1150px){
 .tb-top-grid{grid-template-columns:1fr 1fr}
 .tb-month-card{grid-column:1/-1}
 .tb-work-grid{grid-template-columns:1fr}
}
@media(max-width:720px){
 .tb-top-grid{grid-template-columns:1fr}
 .tb-month-card{grid-column:auto}
 .tb-focus-head{flex-direction:column;align-items:flex-start}
 .tb-task-select{max-width:100%;min-width:100%}
 .tb-task-table-head{display:none}
 .tb-task-row{grid-template-columns:50px 1fr 34px}
 .tb-task-row input:nth-child(2),.tb-task-row select:nth-child(3),.tb-task-row input:nth-child(4),.tb-task-row select:nth-child(5){grid-column:2}
 .tb-status-cards{grid-template-columns:1fr 1fr}
 .tb-day-grid-head,.tb-hour-row{grid-template-columns:55px repeat(3,minmax(90px,1fr))}
 .tb-day-plan-panel{overflow-x:auto}
}


/* V72 SMART DAILY PLANNER */
.tb-date-actions{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.tb-date-actions input{padding:8px 10px;border:1px solid #cbd5e1;border-radius:9px;background:#fff;font-weight:800}
.tb-today-brief{margin-bottom:14px;padding:13px 15px;border-radius:14px;background:linear-gradient(90deg,#fff7cc,#eff6ff);border:1px solid #fde68a}
.tb-today-brief h3{margin:0 0 6px;font-size:15px}.tb-today-brief p{margin:0;color:#475569;font-size:11px;line-height:1.45}
.tb-plan-actions{display:flex;gap:6px;flex-wrap:wrap}
.tb-task-table-head,.tb-task-row{display:grid;grid-template-columns:minmax(220px,1.5fr) 90px 65px 118px 105px 34px;gap:6px;align-items:center}
.tb-task-main{display:grid;grid-template-columns:46px 1fr;gap:6px}
.tb-task-main input{width:100%}
.tb-recurring-list{display:flex;flex-direction:column;gap:7px}
.tb-recurring-row{display:grid;grid-template-columns:minmax(140px,1.4fr) 95px 95px 85px 85px 34px;gap:6px;align-items:center;padding:7px;border:1px solid #e2e8f0;border-radius:10px;background:#fafafa}
.tb-recurring-row input,.tb-recurring-row select{width:100%;padding:7px;border:1px solid #dbe3ea;border-radius:8px;background:#fff;font-size:10px}
.tb-time-slot.routine{background:#fef3c7;border-color:#f59e0b}.tb-time-slot.recurring{background:#f5f3ff;border-color:#8b5cf6}.tb-time-slot.auto{background:#eff6ff;border-color:#60a5fa}
.tb-slot-badge{display:inline-block;margin-left:4px;padding:1px 4px;border-radius:999px;font-size:7.5px;font-weight:800;background:#e2e8f0;color:#475569}
@media(max-width:780px){.tb-task-table-head{display:none}.tb-task-row{grid-template-columns:1fr 34px}.tb-task-main,.tb-task-row select,.tb-task-row input{grid-column:1}.tb-recurring-row{grid-template-columns:1fr 1fr}}


.tb-priority-panel,
.tb-day-plan-panel{
  width:100%;
}
.tb-24-grid{
  height:auto !important;
  max-height:none !important;
  overflow:visible !important;
}
.tb-day-plan-panel .tb-day-grid-head{
  position:sticky;
  top:0;
  z-index:3;
}
.tb-hour-row{
  min-width:0;
}


/* ============================================================
   V74 HEALTH TRACKER
   ============================================================ */
.health-shell{max-width:1500px}
.health-head{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:14px}
.health-date-wrap{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.health-date-wrap input{padding:8px 10px;border:1px solid #cbd5e1;border-radius:9px;background:#fff;font-weight:800}

.health-summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px}
.health-summary-card{padding:18px;border-radius:16px;border:1px solid #e2e8f0;background:#fff}
.health-summary-card span{display:block;font-size:11px;font-weight:800;color:#475569}
.health-summary-card b{display:block;font-size:27px;margin:7px 0 3px;color:#0f172a}
.health-summary-card small{color:#64748b;font-size:10px}
.health-cal-card{background:#fff7ed;border-color:#fdba74}
.health-weight-card{background:#eff6ff;border-color:#93c5fd}
.health-sleep-card{background:#f5f3ff;border-color:#c4b5fd}

.health-panel{margin-bottom:14px}
.health-section-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px}
.health-section-head h2{margin:0 0 3px;font-size:18px}

.health-meal-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.health-meal-tabs button{padding:7px 11px;border-radius:999px;border:1px solid #dbe3ea;background:#eef2f7;font-weight:800;font-size:10px}
.health-meal-tabs button.active{background:#0f172a;color:#fff;border-color:#0f172a}

.health-food-head,.health-food-row{
  display:grid;
  grid-template-columns:105px minmax(220px,1.7fr) 75px 100px 120px 34px;
  gap:7px;
  align-items:center;
}
.health-food-head{padding:7px 4px;border-bottom:1px solid #e2e8f0;color:#64748b;font-size:9.5px;font-weight:800}
.health-food-row{padding:7px 4px;border-bottom:1px solid #f1f5f9}
.health-food-row input,.health-food-row select{width:100%;padding:8px;border:1px solid #dbe3ea;border-radius:8px;background:#fff;font-size:10.5px}
.health-cal-output{font-weight:900;text-align:right;color:#c2410c}
.health-remove-btn{width:30px;height:30px;border-radius:8px;border:1px solid #fecdd3;background:#fff1f2;color:#e11d48;font-weight:900}
.health-calorie-total{display:flex;justify-content:flex-end;align-items:center;gap:14px;margin-top:12px;padding:11px 13px;border-radius:11px;background:#fff7ed;border:1px solid #fed7aa}
.health-calorie-total span{font-size:11px;color:#9a3412;font-weight:700}
.health-calorie-total b{font-size:18px;color:#9a3412}

.health-two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.health-quick-form{display:grid;grid-template-columns:150px 150px auto;gap:9px;align-items:end;margin-bottom:13px}
.health-sleep-form{grid-template-columns:140px 130px 130px auto}
.health-quick-form label{font-size:9.5px;font-weight:800;color:#475569}
.health-quick-form input{display:block;width:100%;margin-top:4px;padding:8px;border:1px solid #cbd5e1;border-radius:8px;background:#fff}

.health-weight-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
.health-weight-stats div{padding:10px;border:1px solid #e2e8f0;border-radius:11px;background:#f8fafc;text-align:center}
.health-weight-stats span{display:block;font-size:9px;color:#64748b}
.health-weight-stats b{display:block;font-size:14px;margin-top:3px}

.health-sleep-preview{display:flex;justify-content:space-between;align-items:center;padding:10px 12px;border-radius:10px;background:#f5f3ff;border:1px solid #ddd6fe;margin-bottom:11px}
.health-sleep-preview span{font-size:10px;color:#6d28d9;font-weight:700}
.health-sleep-preview b{font-size:16px;color:#5b21b6}

.health-weight-chart{min-height:190px;border:1px solid #eef2f7;border-radius:12px;background:#fff;padding:8px;margin-bottom:10px}
.health-small-table{max-height:220px;overflow:auto}
.health-small-table table{width:100%;border-collapse:collapse;font-size:10px}
.health-small-table th{background:#f1f5f9;color:#475569;padding:7px;text-align:left;position:sticky;top:0}
.health-small-table td{padding:7px;border-bottom:1px solid #e5e7eb}
.health-small-table td:last-child,.health-small-table th:last-child{text-align:right}
.health-empty{padding:18px;text-align:center;color:#94a3b8;font-size:10.5px}

@media(max-width:950px){
  .health-summary-grid,.health-two-col{grid-template-columns:1fr}
}
@media(max-width:720px){
  .health-head{align-items:flex-start;flex-direction:column}
  .health-food-head{display:none}
  .health-food-row{grid-template-columns:1fr 1fr}
  .health-food-row select:nth-child(1),.health-food-row input:nth-child(2){grid-column:span 2}
  .health-quick-form,.health-sleep-form{grid-template-columns:1fr 1fr}
}


/* ============================================================
   V75 BRAIN DUMP + PRIORITY PLANNING
   ============================================================ */
.tb-brain-paper{
  position:relative;
  border:1px solid #d7dde7;
  border-radius:14px;
  overflow:hidden;
  background:
    repeating-linear-gradient(
      to bottom,
      #fffdf6 0px,
      #fffdf6 31px,
      #dbe4ef 32px
    );
  box-shadow:inset 46px 0 0 rgba(254,240,138,.22);
}
.tb-brain-paper:before{
  content:"";
  position:absolute;
  top:0;bottom:0;left:45px;
  width:1px;
  background:#fca5a5;
  pointer-events:none;
}
.tb-brain-paper textarea{
  width:100%;
  min-height:190px;
  resize:vertical;
  border:0;
  outline:0;
  padding:8px 18px 34px 58px;
  background:transparent;
  font-family:inherit;
  font-size:14px;
  line-height:32px;
  color:#1f2937;
}
.tb-brain-hint{
  position:absolute;
  left:58px;
  bottom:8px;
  color:#94a3b8;
  font-size:9.5px;
  pointer-events:none;
}

.tb-priority-table-head,
.tb-task-row{
  display:grid !important;
  grid-template-columns:72px minmax(220px,1.5fr) 90px 88px 120px 105px 112px 34px !important;
  gap:7px;
  align-items:center;
}
.tb-priority-table-head{
  padding:8px 5px;
  color:#64748b;
  font-size:9.5px;
  font-weight:800;
  border-bottom:1px solid #e2e8f0;
}
.tb-task-row{
  padding:7px 5px;
  border-bottom:1px solid #f1f5f9;
}
.tb-task-row input,
.tb-task-row select{
  width:100%;
  padding:8px 7px;
  border:1px solid #dbe3ea;
  border-radius:8px;
  background:#fff;
  font-size:10.5px;
}
.tb-task-row .tb-priority-input{
  text-align:center;
  font-weight:900;
}
.tb-task-row.status-Done{background:#f0fdf4}
.tb-task-row.status-Hold{background:#fffbeb}
.tb-task-row.status-Moved{background:#f5f3ff}
.tb-task-row.status-In-Progress{background:#eff6ff}

.tb-time-slot.planned-task{
  background:#ecfeff;
  border-color:#22d3ee;
}
.tb-time-slot.priority-1{background:#fef2f2;border-color:#ef4444}
.tb-time-slot.priority-2{background:#fff7ed;border-color:#f97316}
.tb-time-slot.priority-3{background:#fffbeb;border-color:#eab308}
.tb-planned-task-title{
  display:block;
  font-size:9.5px;
  font-weight:800;
  margin-top:3px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.tb-planned-task-meta{
  display:block;
  margin-top:2px;
  font-size:8px;
  color:#64748b;
}

@media(max-width:900px){
  .tb-priority-table-head{display:none}
  .tb-task-row{
    grid-template-columns:70px 1fr 34px !important;
  }
  .tb-task-row > *:not(.tb-delete-task){
    grid-column:1 / span 2;
  }
  .tb-task-row .tb-priority-input{grid-column:1}
}


/* ============================================================
   V76 LIVE 24-HOUR PRIORITY PLANNING
   ============================================================ */
.tb-live-plan-legend{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin-top:6px;
  font-size:9px;
  color:#64748b;
}
.tb-live-plan-legend span{display:flex;align-items:center;gap:4px}
.tb-live-plan-legend i{width:9px;height:9px;border-radius:3px;display:inline-block}
.tb-live-plan-legend .fixed{background:#22d3ee}
.tb-live-plan-legend .priority{background:#f59e0b}
.tb-live-plan-legend .tentative{background:#94a3b8}
.tb-live-plan-legend .routine{background:#fde68a}

.tb-time-slot.tentative-task{
  background:#f8fafc;
  border:1px dashed #94a3b8;
}
.tb-time-slot.auto-priority{
  background:#fff7ed;
  border-color:#fb923c;
}
.tb-time-slot.auto-priority.priority-1{
  background:#fef2f2;
  border-color:#ef4444;
}
.tb-time-slot.auto-priority.priority-2{
  background:#fff7ed;
  border-color:#f97316;
}
.tb-time-slot.auto-priority.priority-3{
  background:#fffbeb;
  border-color:#eab308;
}
.tb-slot-badge.tentative-badge{
  background:#e2e8f0;
  color:#475569;
}


/* ============================================================
   V77 TASK STATUS DASHBOARD
   ============================================================ */
.tb-status-dashboard{margin-bottom:14px}
.tb-status-top-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:12px}
.tb-status-top-head h2{margin:0 0 3px;font-size:18px}
.tb-status-total{padding:7px 11px;border-radius:999px;background:#f1f5f9;color:#334155;font-size:10px;font-weight:800}

.tb-status-summary-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}
.tb-status-summary-card{
  text-align:left;
  padding:13px;
  border-radius:13px;
  border:1px solid #e2e8f0;
  background:#fff;
  cursor:pointer;
  transition:.15s ease;
}
.tb-status-summary-card:hover{transform:translateY(-1px);box-shadow:0 6px 15px rgba(15,23,42,.06)}
.tb-status-summary-card span{display:block;font-size:10px;font-weight:800;color:#334155}
.tb-status-summary-card b{display:block;font-size:24px;margin:4px 0}
.tb-status-summary-card small{display:block;font-size:9px;color:#64748b}
.tb-status-summary-card.not-started{background:#f8fafc}
.tb-status-summary-card.in-progress{background:#eff6ff;border-color:#93c5fd}
.tb-status-summary-card.done{background:#f0fdf4;border-color:#86efac}
.tb-status-summary-card.hold{background:#fffbeb;border-color:#fde68a}
.tb-status-summary-card.moved{background:#f5f3ff;border-color:#c4b5fd}

.tb-status-analytics-panel{margin-bottom:14px}
.tb-analytics-tabs{display:flex;gap:6px;flex-wrap:wrap}
.tb-analytics-tabs button{
  padding:7px 10px;border:1px solid #dbe3ea;border-radius:999px;background:#eef2f7;
  color:#334155;font-size:10px;font-weight:800
}
.tb-analytics-tabs button.active{background:#0f172a;color:#fff;border-color:#0f172a}
.tb-analytics-summary-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:12px}
.tb-analytics-summary-card{padding:10px;border:1px solid #e2e8f0;border-radius:11px;background:#f8fafc}
.tb-analytics-summary-card span{display:block;font-size:9px;color:#64748b}
.tb-analytics-summary-card b{display:block;font-size:18px;margin-top:3px;color:#0f172a}
.tb-analytics-chart{min-height:220px;border:1px solid #eef2f7;border-radius:12px;background:#fff;padding:10px}
.tb-analytics-details{margin-top:10px;overflow:auto}
.tb-analytics-details table{width:100%;border-collapse:collapse;font-size:10px}
.tb-analytics-details th{background:#f1f5f9;padding:7px;text-align:left;color:#475569}
.tb-analytics-details td{padding:7px;border-bottom:1px solid #e5e7eb}
.tb-analytics-details td:not(:first-child),.tb-analytics-details th:not(:first-child){text-align:right}

@media(max-width:900px){
  .tb-status-summary-grid,.tb-analytics-summary-grid{grid-template-columns:repeat(2,1fr)}
}


/* ============================================================
   V78 SMART DAY WINDOWS + PERSISTENT BRAIN DUMP
   ============================================================ */
.tb-remaining-card #tbCurrentClock{
  font-variant-numeric:tabular-nums;
  letter-spacing:.03em;
}
.tb-brain-paper textarea{
  min-height:220px;
}

.tb-sleep-strip{
  display:grid;
  grid-template-columns:1fr auto auto;
  gap:12px;
  align-items:center;
  padding:10px 13px;
  margin-bottom:10px;
  border-radius:11px;
  background:#f5f3ff;
  border:1px solid #ddd6fe;
  color:#5b21b6;
  font-size:10px;
}
.tb-sleep-strip span{font-weight:800}
.tb-sleep-strip b{font-size:11px}
.tb-sleep-strip small{color:#7c3aed}

.tb-smart-day-windows{
  display:flex;
  flex-direction:column;
  gap:12px;
}
.tb-day-window{
  border:1px solid #e2e8f0;
  border-radius:14px;
  overflow:hidden;
  background:#fff;
}
.tb-day-window.current-window{
  border-color:#60a5fa;
  box-shadow:0 0 0 2px rgba(96,165,250,.10);
}
.tb-window-head{
  display:flex;
  justify-content:space-between;
  gap:12px;
  align-items:center;
  padding:10px 12px;
  background:#f8fafc;
  border-bottom:1px solid #e2e8f0;
}
.tb-window-head strong{font-size:12px}
.tb-window-head span{font-size:9.5px;color:#64748b}
.tb-window-head .tb-window-now{
  padding:3px 7px;
  border-radius:999px;
  background:#dbeafe;
  color:#1d4ed8;
  font-size:8.5px;
  font-weight:800;
}
.tb-window-grid-head,
.tb-window-hour-row{
  display:grid;
  grid-template-columns:76px repeat(3,1fr);
  gap:6px;
  align-items:stretch;
}
.tb-window-grid-head{
  padding:7px 8px;
  color:#64748b;
  font-size:9px;
  font-weight:800;
  border-bottom:1px solid #f1f5f9;
}
.tb-window-hour-row{
  padding:5px 8px;
  border-bottom:1px solid #f1f5f9;
}
.tb-window-hour-row:last-child{border-bottom:0}
.tb-window-hour-label{
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:8px;
  background:#f8fafc;
  font-size:10px;
  font-weight:900;
  color:#475569;
}
.tb-window-hour-row.current-hour .tb-window-hour-label{
  background:#dbeafe;
  color:#1d4ed8;
}
.tb-smart-day-windows .tb-time-slot{
  min-height:42px;
}
@media(max-width:720px){
  .tb-window-grid-head,.tb-window-hour-row{
    grid-template-columns:58px repeat(3,minmax(100px,1fr));
  }
  .tb-day-window{overflow-x:auto}
}


/* ============================================================
   V79 BRAIN DUMP + STATUS DETAIL FIXES
   ============================================================ */
.tb-status-details-box{
  width:min(1050px,96%);
  max-height:88vh;
  overflow:auto;
}
.tb-status-details-summary{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:8px;
  margin:14px 0;
}
.tb-status-details-summary div{
  padding:10px;
  border:1px solid #e2e8f0;
  border-radius:11px;
  background:#f8fafc;
}
.tb-status-details-summary span{
  display:block;
  font-size:9px;
  color:#64748b;
}
.tb-status-details-summary b{
  display:block;
  margin-top:3px;
  font-size:16px;
}
.tb-status-details-table{
  overflow:auto;
  border:1px solid #e2e8f0;
  border-radius:12px;
}
.tb-status-details-table table{
  width:100%;
  border-collapse:collapse;
  font-size:10.5px;
}
.tb-status-details-table th{
  position:sticky;
  top:0;
  background:#eff6ff;
  color:#334155;
  padding:9px 8px;
  text-align:left;
  border-bottom:1px solid #cbd5e1;
}
.tb-status-details-table td{
  padding:9px 8px;
  border-bottom:1px solid #e5e7eb;
}
.tb-status-details-table td:nth-child(1){
  font-weight:800;
}
.tb-status-details-time{
  white-space:nowrap;
  font-weight:700;
}
.tb-status-no-time{
  color:#94a3b8;
}
@media(max-width:720px){
  .tb-status-details-summary{grid-template-columns:repeat(2,1fr)}
}


/* ============================================================
   V82 RECURRING TASK TRACKING
   ============================================================ */
.tb-recurring-card{
  border:1px solid #e2e8f0;
  border-radius:14px;
  padding:14px;
  background:#fff;
}
.tb-recurring-summary{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:9px;
  margin-bottom:12px;
}
.tb-recurring-summary button{
  text-align:left;
  padding:11px 12px;
  border:1px solid #e2e8f0;
  border-radius:11px;
  background:#f8fafc;
  cursor:pointer;
}
.tb-recurring-summary button.done{
  background:#f0fdf4;
  border-color:#86efac;
}
.tb-recurring-summary button.pending{
  background:#fff7ed;
  border-color:#fdba74;
}
.tb-recurring-summary span{
  display:block;
  font-size:9px;
  color:#64748b;
  font-weight:800;
}
.tb-recurring-summary b{
  display:block;
  margin:3px 0;
  font-size:21px;
}
.tb-recurring-summary small{
  font-size:8.5px;
  color:#94a3b8;
}

.tb-recurring-head,
.tb-recurring-row{
  display:grid !important;
  grid-template-columns:minmax(180px,1.6fr) 90px 120px 90px 82px 100px 120px 34px !important;
  gap:7px;
  align-items:center;
}
.tb-recurring-head{
  padding:7px 5px;
  border-bottom:1px solid #e2e8f0;
  color:#64748b;
  font-size:9px;
  font-weight:800;
}
.tb-recurring-row{
  padding:7px 5px !important;
  border-bottom:1px solid #f1f5f9 !important;
  border-radius:0 !important;
  background:#fff !important;
}
.tb-recurring-row input,
.tb-recurring-row select{
  width:100%;
  padding:7px !important;
  border:1px solid #dbe3ea;
  border-radius:8px;
  background:#fff;
  font-size:10px;
}
.tb-recurring-status{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:4px;
}
.tb-recurring-status button{
  padding:6px 5px;
  border-radius:7px;
  border:1px solid #dbe3ea;
  background:#f8fafc;
  font-size:8.5px;
  font-weight:800;
}
.tb-recurring-status button.active-done{
  background:#dcfce7;
  border-color:#22c55e;
  color:#166534;
}
.tb-recurring-status button.active-pending{
  background:#ffedd5;
  border-color:#fb923c;
  color:#9a3412;
}

.tb-recurring-details-box{
  width:min(950px,96%);
  max-height:88vh;
  overflow:auto;
}
.tb-recurring-detail-table{
  width:100%;
  border-collapse:collapse;
  font-size:10.5px;
}
.tb-recurring-detail-table th{
  background:#f1f5f9;
  padding:9px;
  text-align:left;
  color:#475569;
  position:sticky;
  top:0;
}
.tb-recurring-detail-table td{
  padding:9px;
  border-bottom:1px solid #e5e7eb;
}
.tb-recurring-detail-status.done{
  color:#15803d;
  font-weight:900;
}
.tb-recurring-detail-status.pending{
  color:#c2410c;
  font-weight:900;
}
.tb-routine-clickable{
  cursor:pointer;
}
.tb-routine-clickable:hover{
  filter:brightness(.98);
}

@media(max-width:950px){
  .tb-recurring-head{display:none}
  .tb-recurring-row{
    grid-template-columns:1fr 1fr !important;
    border:1px solid #e2e8f0 !important;
    border-radius:10px !important;
    margin-bottom:7px;
  }
}


/* V83 LEARNING TRACKER */
.lr-shell{max-width:1500px}.lr-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:14px}
.lr-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}
.lr-summary>div{padding:15px;border:1px solid #dbeafe;border-radius:14px;background:linear-gradient(135deg,#f8fbff,#fff)}
.lr-summary span{display:block;font-size:9px;color:#64748b;font-weight:800}.lr-summary b{display:block;font-size:23px;margin:4px 0}.lr-summary small{color:#94a3b8;font-size:8.5px}
.lr-section-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:11px}.lr-section-head h2{margin:0 0 3px;font-size:18px}.lr-mt{margin-top:18px}
.lr-skill-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:9px}
.lr-skill-card{padding:13px;border:1px solid #e2e8f0;border-radius:12px;background:#fff;text-align:left;cursor:pointer}.lr-skill-card.active{background:#eff6ff;border-color:#60a5fa}
.lr-skill-card .ico{font-size:22px}.lr-skill-card h3{margin:5px 0 3px}.lr-skill-card p{margin:0;color:#64748b;font-size:9px}.lr-mini{height:6px;background:#e2e8f0;border-radius:999px;margin-top:8px;overflow:hidden}.lr-mini span{display:block;height:100%;background:#2563eb}
.lr-overview{margin-top:14px}.lr-overview-top{display:flex;justify-content:space-between;gap:12px;align-items:center}.lr-chip{padding:4px 7px;border-radius:999px;background:#dbeafe;color:#1d4ed8;font-size:8px;font-weight:900}
.lr-progress-circle{width:80px;height:80px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(#2563eb 0deg,#e2e8f0 0deg);position:relative}.lr-progress-circle:before{content:"";position:absolute;width:60px;height:60px;background:#fff;border-radius:50%}.lr-progress-circle span{z-index:1;font-weight:900}.lr-progress-wrap{text-align:center}.lr-progress-wrap small{font-size:8px;color:#64748b}
.lr-overview-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:13px}.lr-overview-stats div{padding:9px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;text-align:center}.lr-overview-stats span{display:block;font-size:8px;color:#64748b}.lr-overview-stats b{display:block;margin-top:2px;font-size:13px}
.lr-two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.lr-continue{padding:13px;border-radius:12px;background:#eff6ff;border:1px solid #bfdbfe}.lr-continue h3{margin:0 0 4px}.lr-continue p{font-size:9.5px;color:#64748b}
.lr-goal-row{display:grid;grid-template-columns:90px auto auto;gap:7px;align-items:center}.lr-goal-row input{padding:8px;border:1px solid #cbd5e1;border-radius:8px}.lr-goal-row span{font-size:9px;color:#64748b}
.lr-goal-bar{height:8px;background:#e2e8f0;border-radius:999px;overflow:hidden;margin-top:10px}.lr-goal-bar span{display:block;height:100%;background:#22c55e}.lr-goal-cap{display:flex;justify-content:space-between;font-size:8.5px;color:#64748b;margin-top:4px}
.lr-note{width:100%;min-height:150px;border:1px solid #dbe3ea;border-radius:10px;padding:10px;background:#fffdf7;resize:vertical}.lr-note-foot{display:flex;justify-content:space-between;align-items:center;margin-top:6px;font-size:8.5px;color:#64748b}
.lr-filters{display:flex;gap:5px;flex-wrap:wrap}.lr-filters button{padding:6px 8px;border-radius:999px;border:1px solid #dbe3ea;background:#eef2f7;font-size:8.5px;font-weight:800}.lr-filters button.active{background:#0f172a;color:#fff}
.lr-roadmap{display:flex;flex-direction:column;gap:8px}.lr-stage{border:1px solid #e2e8f0;border-radius:12px;overflow:hidden}.lr-stage-head{padding:9px 11px;background:#f8fafc;border-bottom:1px solid #e2e8f0;display:flex;justify-content:space-between;font-size:10px;font-weight:800}.lr-stage-head span{color:#64748b;font-size:8.5px}
.lr-topic{display:grid;grid-template-columns:1fr 125px 105px;gap:8px;align-items:center;padding:9px 11px;border-bottom:1px solid #f1f5f9}.lr-topic:last-child{border-bottom:0}.lr-topic b{display:block;font-size:10px}.lr-topic small{display:block;color:#64748b;font-size:8px;margin-top:2px}.lr-topic select,.lr-topic input{width:100%;padding:7px;border:1px solid #dbe3ea;border-radius:8px;font-size:9px}
.lr-projects{display:flex;flex-direction:column;gap:7px}.lr-project{display:grid;grid-template-columns:1fr 110px 32px;gap:7px;align-items:center}.lr-project input,.lr-project select{padding:7px;border:1px solid #dbe3ea;border-radius:8px;font-size:9px}
.lr-review{padding:9px;border:1px solid #fde68a;background:#fffbeb;border-radius:9px;margin-bottom:6px}.lr-review b{font-size:10px}.lr-review span{display:block;font-size:8px;color:#92400e;margin-top:2px}
#lrHistory table{width:100%;border-collapse:collapse;font-size:9.5px}#lrHistory th{background:#f1f5f9;padding:7px;text-align:left}#lrHistory td{padding:7px;border-bottom:1px solid #e5e7eb}
@media(max-width:900px){.lr-summary,.lr-overview-stats{grid-template-columns:repeat(2,1fr)}.lr-two-col{grid-template-columns:1fr}}@media(max-width:700px){.lr-head,.lr-overview-top{flex-direction:column;align-items:flex-start}.lr-topic{grid-template-columns:1fr}}


/* V84 FULL PAGE LEARNING NOTES */
.lr-head-actions{display:flex;gap:8px;flex-wrap:wrap}
.lr-notes-launch{padding:10px 15px;border-radius:10px;border:1px solid #f59e0b;background:#fffbeb;color:#92400e;font-weight:900;cursor:pointer}
.lr-notes-page{display:none;position:fixed;inset:0;z-index:5000;background:#f8fafc;overflow:hidden}
.lr-notes-page.open{display:flex;flex-direction:column}
.lr-notes-topbar{min-height:72px;padding:12px 18px;border-bottom:1px solid #e2e8f0;background:#fff;display:flex;justify-content:space-between;gap:14px;align-items:center}
.lr-notes-top-left{display:flex;align-items:center;gap:12px}.lr-notes-top-left h2{margin:0;font-size:20px}.lr-notes-top-left p{margin:3px 0 0;color:#64748b;font-size:9.5px}
.lr-notes-actions{display:flex;gap:7px;align-items:center;flex-wrap:wrap}.lr-save-state{padding:6px 9px;border-radius:999px;background:#dcfce7;color:#166534;font-size:9px;font-weight:900}.lr-save-state.unsaved{background:#fef3c7;color:#92400e}.lr-import-label{cursor:pointer}.lr-import-label input{display:none}
.lr-notes-layout{flex:1;min-height:0;display:grid;grid-template-columns:280px 1fr}.lr-notes-sidebar{border-right:1px solid #e2e8f0;background:#fff;padding:12px;overflow:auto}
.lr-notes-sidebar-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px}.lr-notes-search{width:100%;padding:9px;border:1px solid #dbe3ea;border-radius:9px;margin-bottom:9px}
.lr-notes-list{display:flex;flex-direction:column;gap:6px}.lr-note-list-item{width:100%;text-align:left;padding:10px;border:1px solid #e2e8f0;border-radius:10px;background:#fff;cursor:pointer}.lr-note-list-item.active{background:#eff6ff;border-color:#60a5fa}.lr-note-list-item b{display:block;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.lr-note-list-item span,.lr-note-list-item small{display:block;margin-top:3px;font-size:8px;color:#64748b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lr-notes-editor{min-width:0;display:flex;flex-direction:column;padding:18px 22px;overflow:hidden}.lr-note-meta-row{display:grid;grid-template-columns:minmax(250px,1fr) 180px 150px;gap:8px;margin-bottom:8px}.lr-note-meta-row input,.lr-note-meta-row select{padding:9px;border:1px solid #dbe3ea;border-radius:9px;background:#fff}.lr-full-note-title{font-size:18px!important;font-weight:900}
.lr-note-toolbar{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px}.lr-note-toolbar button{padding:6px 9px;border:1px solid #dbe3ea;border-radius:7px;background:#fff;font-size:9px;font-weight:800}
.lr-full-note-body{flex:1;width:100%;min-height:0;resize:none;padding:18px 22px;border:1px solid #dbe3ea;border-radius:12px;outline:none;background:repeating-linear-gradient(to bottom,#fffdf7 0px,#fffdf7 31px,#e5e7eb 32px);font-family:inherit;font-size:14px;line-height:32px}.lr-full-note-body:focus{border-color:#60a5fa;box-shadow:0 0 0 2px rgba(96,165,250,.1)}
.lr-notes-footer{display:flex;justify-content:space-between;gap:10px;padding-top:7px;color:#64748b;font-size:8.5px}
@media(max-width:820px){.lr-notes-layout{grid-template-columns:1fr}.lr-notes-sidebar{display:none}.lr-note-meta-row{grid-template-columns:1fr}.lr-notes-topbar{align-items:flex-start;flex-direction:column}}


.lr-cloud-state{
  padding:6px 9px;
  border-radius:999px;
  background:#eef2ff;
  color:#4338ca;
  font-size:9px;
  font-weight:900;
}
.lr-cloud-state.ok{background:#dcfce7;color:#166534}
.lr-cloud-state.wait{background:#fef3c7;color:#92400e}
.lr-cloud-state.err{background:#fee2e2;color:#b91c1c}


/* V86 TIME COMMAND CENTER */
.tb-command-center{display:grid;grid-template-columns:repeat(5,minmax(145px,1fr));gap:10px;margin:14px 0}.tb-command-btn{border:1px solid #dbe3ea;border-radius:14px;background:#fff;padding:13px 12px;text-align:left;cursor:pointer;transition:.15s}.tb-command-btn:hover{transform:translateY(-1px);box-shadow:0 8px 18px rgba(15,23,42,.07);border-color:#93c5fd}.tb-command-btn.active{background:#eff6ff;border-color:#60a5fa}.tb-command-btn.primary-command{background:#eef6ff;border-color:#93c5fd}.tb-command-btn span{display:block;font-size:22px;margin-bottom:5px}.tb-command-btn b{display:block;font-size:11px}.tb-command-btn small{display:block;font-size:8.5px;color:#64748b;margin-top:2px}.tb-tool-panel{display:none!important}.tb-tool-panel.tb-tool-open{display:block!important}#tbQuickPanel.tb-tool-open{display:grid!important}.tb-status-summary-grid{grid-template-columns:repeat(auto-fit,minmax(145px,1fr))!important}.tb-status-summary-card.skipped{background:#fff1f2;border-color:#fda4af}.tb-status-summary-card.follow-up{background:#ecfeff;border-color:#67e8f9}.tb-status-details-table input,.tb-status-details-table select{width:100%;min-width:75px;padding:6px;border:1px solid #dbe3ea;border-radius:7px;background:#fff;font-size:9.5px}.tb-inline-task{min-width:180px}.tb-inline-priority{width:60px;text-align:center;font-weight:900}.tb-inline-actions{white-space:nowrap}.tb-inline-actions button{padding:5px 7px;border:1px solid #dbe3ea;border-radius:7px;margin:2px;font-size:8.5px;font-weight:800;cursor:pointer}.tb-inline-actions .done{background:#dcfce7;color:#166534}.tb-inline-actions .hold{background:#fffbeb;color:#92400e}.tb-inline-actions .skip{background:#fff1f2;color:#be123c}.tb-inline-actions .follow{background:#ecfeff;color:#0e7490}@media(max-width:900px){.tb-command-center{grid-template-columns:repeat(2,1fr)}}

/* V87 TIME WORKFLOW FIX */
.tb-panel-close-row{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:8px 10px;margin-bottom:10px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0}
.tb-panel-close-row-grid{grid-column:1/-1}.tb-panel-close-row b{font-size:11px}.tb-panel-close-row button{padding:6px 9px;border-radius:8px;border:1px solid #fecaca;background:#fff1f2;color:#be123c;font-size:8.5px;font-weight:900;cursor:pointer}
.tb-smart-task-click{cursor:pointer}.tb-smart-task-click:hover{outline:2px solid rgba(37,99,235,.18);border-radius:7px}
.tb-task-editor-box{width:min(900px,96%)}.tb-task-editor-grid{display:grid;grid-template-columns:2fr .7fr 1fr .8fr 1.1fr 1fr 1.1fr;gap:8px;margin:14px 0}.tb-task-editor-grid label{font-size:8.5px;font-weight:800;color:#64748b}.tb-task-editor-grid input,.tb-task-editor-grid select{display:block;width:100%;margin-top:4px;padding:8px;border:1px solid #cbd5e1;border-radius:8px;background:#fff}
.tb-task-editor-actions{display:flex;gap:7px;flex-wrap:wrap}.tb-task-editor-actions button{padding:8px 10px;border-radius:8px;border:1px solid #dbe3ea;font-weight:800;cursor:pointer}.tb-task-editor-actions .done{background:#dcfce7;color:#166534}.tb-task-editor-actions .hold{background:#fef3c7;color:#92400e}.tb-task-editor-actions .skip{background:#ffe4e6;color:#be123c}.tb-task-editor-actions .follow{background:#cffafe;color:#0e7490}.tb-task-editor-actions .delete{background:#fee2e2;color:#b91c1c}
@media(max-width:900px){.tb-task-editor-grid{grid-template-columns:1fr 1fr}}


/* V88 SIMPLIFIED TASK WORKFLOW */
.tb-status-summary-grid{grid-template-columns:repeat(4,minmax(170px,1fr))!important}
.tb-status-summary-card.not-started{background:#f8fafc!important;border-color:#cbd5e1!important}
.tb-status-summary-card.in-progress{background:#fff7cc!important;border-color:#facc15!important}
.tb-status-summary-card.done{background:#dcfce7!important;border-color:#22c55e!important}
.tb-status-summary-card.hold{background:#fee2e2!important;border-color:#ef4444!important}
.tb-task-editor-actions .start{background:#fef9c3;color:#854d0e}
.tb-task-editor-actions .done{background:#dcfce7;color:#166534}
.tb-task-editor-actions .hold{background:#fee2e2;color:#b91c1c}
.tb-task-editor-actions .delete{background:#f3f4f6;color:#111827}
.tb-edit-timestamp-info{margin-top:12px;padding:10px 12px;border-radius:10px;background:#f8fafc;border:1px solid #e2e8f0;font-size:9px;color:#475569;line-height:1.7}
.tb-status-details-table .tb-inline-actions button.start{background:#fef9c3;border-color:#fde047;color:#854d0e}
.tb-status-details-table .tb-inline-actions button.done{background:#dcfce7;border-color:#86efac;color:#166534}
.tb-status-details-table .tb-inline-actions button.hold{background:#fee2e2;border-color:#fca5a5;color:#b91c1c}
.tb-status-details-table .tb-inline-actions button.delete{background:#f3f4f6;border-color:#d1d5db;color:#111827}
@media(max-width:900px){.tb-status-summary-grid{grid-template-columns:repeat(2,1fr)!important}}


/* ============================================================
   V89 STATUS POPUP / TOP3 FIX
   ============================================================ */
.tb-status-summary-card{
  cursor:pointer !important;
  pointer-events:auto !important;
  position:relative;
  z-index:1;
}
#tbStatusDetailsModal{
  z-index:12000 !important;
}
#tbStatusDetailsModal .modal-box{
  position:relative;
  z-index:12001;
}
.tb-status-modal-close{
  cursor:pointer;
}


/* V90 Task popup runtime fix */
#tbStatusDetailsModal .modal-box{
  width:min(1450px,96vw) !important;
  max-height:88vh;
  overflow:auto;
}
#tbStatusDetailsTable{
  overflow:auto;
}
#tbStatusDetailsTable table{
  min-width:1250px;
}


.tb-status-details-table .tb-inline-actions button:active{
  transform:translateY(1px);
  filter:brightness(.96);
}

/* V92 real-time popup refresh */
#tbStatusDetailsTable tbody tr{
  transition:opacity .12s ease, transform .12s ease;
}
.tb-status-details-table .tb-inline-actions button{
  cursor:pointer !important;
}

/* V93 true live task updates */
#tbStatusDetailsTable tbody tr{
  transition:opacity .09s ease,transform .09s ease;
}
#tbStatusDetailsTable .tb-inline-actions button{
  user-select:none;
}

/* V94 guaranteed live updates */
#tbStatusDetailsSummary b{
  transition:transform .12s ease;
}
#tbStatusDetailsTable tbody tr{
  transition:opacity .09s ease,transform .09s ease;
}

/* ============================================================
   V95 BRAIN DUMP — DUPLICATES + REFRESH
   ============================================================ */
.tb-brain-refresh-btn{
  border:1px solid #93c5fd;
  background:#eff6ff;
  color:#1d4ed8;
  border-radius:9px;
  padding:8px 11px;
  font-size:9px;
  font-weight:900;
  cursor:pointer;
  white-space:nowrap;
}
.tb-brain-refresh-btn:hover{background:#dbeafe}
.tb-task-title-wrap{
  display:flex;
  align-items:center;
  gap:6px;
}
.tb-task-title-wrap .tb-inline-task{
  flex:1;
  min-width:140px;
}
.tb-occurrence-tag{
  flex:0 0 auto;
  min-width:34px;
  text-align:center;
  padding:4px 6px;
  border-radius:999px;
  background:#eef2ff;
  border:1px solid #c7d2fe;
  color:#4338ca;
  font-size:8px;
  font-weight:900;
}


/* ============================================================
   V96 RECURRING RULES
   ============================================================ */
.tb-recurring-filter-row{
  display:flex;gap:6px;flex-wrap:wrap;margin:12px 0;
}
.tb-recurring-filter-row button{
  padding:7px 10px;border:1px solid #dbe3ea;border-radius:999px;
  background:#f8fafc;font-size:8.5px;font-weight:900;cursor:pointer;
}
.tb-recurring-filter-row button.active{background:#0f172a;color:#fff;border-color:#0f172a}

.tb-recurring-brain{
  margin:12px 0 16px;
  background:linear-gradient(135deg,#fffdf7,#fff);
}
.tb-recurring-brain h3{margin:0 0 3px;font-size:15px}
.tb-recurring-brain-controls{
  display:grid;
  grid-template-columns:1.15fr 1.35fr 1fr .8fr 1fr;
  gap:8px;
  margin-bottom:9px;
}
.tb-recurring-brain-controls label{font-size:8px;font-weight:900;color:#64748b}
.tb-recurring-brain-controls input,
.tb-recurring-brain-controls select{
  width:100%;display:block;margin-top:4px;padding:8px;
  border:1px solid #dbe3ea;border-radius:8px;background:#fff;
}
.tb-recurring-brain-input{
  width:100%;min-height:95px;resize:vertical;padding:12px;
  border:1px solid #dbe3ea;border-radius:10px;background:#fffdf7;
  line-height:24px;
}
.tb-recurring-head-v96,
.tb-recurring-row-v96{
  grid-template-columns:2fr 1.1fr 1.4fr .9fr .7fr 1fr .7fr 38px !important;
}
.tb-recurring-row-v96 .tb-active-toggle{
  display:flex;align-items:center;justify-content:center;
}
.tb-recurring-row-v96 input[type="checkbox"]{width:18px;height:18px}
.tb-recurring-occurrence-badge{
  display:inline-block;margin-left:5px;padding:2px 5px;border-radius:999px;
  background:#dbeafe;color:#1d4ed8;font-size:7.5px;font-weight:900;
}
@media(max-width:900px){
  .tb-recurring-brain-controls{grid-template-columns:1fr 1fr}
}


/* V97 Smart Time + Period Status */
.tb-status-period-row{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0 14px}
.tb-status-period-row button{padding:7px 11px;border:1px solid #dbe3ea;border-radius:999px;background:#f8fafc;font-size:8.5px;font-weight:900;cursor:pointer}
.tb-status-period-row button.active{background:#0f172a;color:#fff;border-color:#0f172a}
.tb-projection-note{padding:9px 11px;margin-bottom:10px;border:1px solid #bfdbfe;background:#eff6ff;color:#1e3a8a;border-radius:9px;font-size:8.5px}
.tb-source-pill{display:inline-block;padding:2px 6px;border-radius:999px;background:#f1f5f9;color:#475569;font-size:7.5px;font-weight:900}
.tb-source-pill.recurring{background:#dbeafe;color:#1d4ed8}
.tb-smart-list{display:flex;flex-direction:column;gap:8px;padding:10px 0}
.tb-smart-task-row{display:grid;grid-template-columns:72px minmax(180px,2fr) 110px 90px 80px 110px 130px;gap:8px;align-items:center;padding:10px;border:1px solid #e2e8f0;border-radius:11px;background:#fff}
.tb-smart-task-row.in-progress{background:#fff7cc;border-color:#facc15}
.tb-smart-task-row.done{background:#dcfce7;border-color:#22c55e}
.tb-smart-task-row.hold{background:#fee2e2;border-color:#ef4444}
.tb-smart-task-row input,.tb-smart-task-row select{width:100%;padding:7px;border:1px solid #cbd5e1;border-radius:7px;background:#fff}
.tb-smart-task-row .tb-smart-end{text-align:center;font-weight:900}
.tb-smart-task-row .tb-source-pill{text-align:center}
.tb-smart-empty{padding:20px;text-align:center;border:1px dashed #cbd5e1;border-radius:12px;color:#64748b}
@media(max-width:1000px){.tb-smart-task-row{grid-template-columns:1fr 1fr}}


/* ============================================================
   V98 MONTHLY LIFE REVIEW
   ============================================================ */
.review-page{display:flex;flex-direction:column;gap:16px}
.review-header{display:flex;justify-content:space-between;align-items:center;gap:14px}
.review-header h1{margin:0 0 5px}
.review-date-controls{display:flex;gap:7px;align-items:center;flex-wrap:wrap}
.review-date-controls select{padding:9px 12px;border:1px solid #dbe3ea;border-radius:9px;background:#fff;font-weight:800}

.review-summary-grid{display:grid;grid-template-columns:repeat(7,minmax(130px,1fr));gap:10px}
.rv-summary{border:1px solid #dbe3ea;border-radius:14px;background:#fff;padding:13px;text-align:left;cursor:pointer}
.rv-summary span,.rv-summary small{display:block}.rv-summary span{font-size:9px;font-weight:900}.rv-summary b{display:block;font-size:20px;margin:6px 0}.rv-summary small{font-size:7.5px;color:#64748b}
.rv-summary.income{background:#ecfdf5;border-color:#86efac}.rv-summary.expense{background:#fff1f2;border-color:#fda4af}.rv-summary.saving{background:#eff6ff;border-color:#93c5fd}
.rv-summary.sleep{background:#f5f3ff;border-color:#c4b5fd}.rv-summary.task{background:#f0fdf4;border-color:#86efac}.rv-summary.calorie{background:#fff7ed;border-color:#fdba74}.rv-summary.weight{background:#f8fafc}

.rv-calendar-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}
.rv-calendar-head h2{margin:0}.rv-legend{display:flex;gap:8px;flex-wrap:wrap;font-size:7.5px;color:#64748b}
.rv-week-head,.rv-calendar-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}
.rv-week-head span{padding:7px;text-align:center;font-size:8px;font-weight:900;color:#64748b}
.rv-day{min-height:128px;border:1px solid #e2e8f0;border-radius:11px;background:#fff;padding:8px;cursor:pointer;overflow:hidden}
.rv-day:hover{border-color:#60a5fa;box-shadow:0 5px 14px rgba(15,23,42,.06)}
.rv-day.outside{opacity:.3}.rv-day.today{outline:2px solid #2563eb}
.rv-day-num{font-weight:900;font-size:10px;margin-bottom:6px}
.rv-day-lines{display:flex;flex-direction:column;gap:3px;font-size:7.5px}
.rv-day-lines span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rv-day-lines .good{color:#15803d}.rv-day-lines .bad{color:#dc2626}.rv-day-lines .neutral{color:#475569}

.rv-trend-bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(36px,1fr));gap:5px;align-items:end;min-height:210px;padding:12px 4px}
.rv-trend-day{display:flex;flex-direction:column;align-items:center;gap:4px}
.rv-trend-stack{height:150px;width:100%;display:flex;align-items:end;justify-content:center;gap:2px}
.rv-trend-stack i{display:block;width:7px;border-radius:5px 5px 0 0;background:currentColor}
.rv-trend-day small{font-size:7px;color:#64748b}

.rv-day-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px}
.rv-day-summary div{padding:10px;border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}
.rv-day-summary span,.rv-day-summary b{display:block}.rv-day-summary span{font-size:7.5px;color:#64748b}.rv-day-summary b{font-size:15px;margin-top:3px}
.rv-day-table{width:100%;border-collapse:collapse}.rv-day-table th,.rv-day-table td{padding:7px;border-bottom:1px solid #e2e8f0;text-align:left;font-size:8.5px}
.rv-day-modal-box{width:min(1100px,95vw);max-height:88vh;overflow:auto}

@media(max-width:1200px){.review-summary-grid{grid-template-columns:repeat(4,1fr)}}
@media(max-width:800px){.review-summary-grid{grid-template-columns:repeat(2,1fr)}.review-header{align-items:flex-start;flex-direction:column}.rv-day{min-height:100px}}


/* ============================================================
   V99 REVIEW — INTEGRATED & EDITABLE
   ============================================================ */
.review-shell{max-width:1500px}
.review-page{display:flex;flex-direction:column;gap:16px}
.review-header{
  display:grid !important;
  grid-template-columns:minmax(0,1fr) auto;
  align-items:center !important;
  gap:20px;
}
.review-title-wrap h1{margin:0 0 5px;font-size:28px}
.review-title-wrap p{margin:0}
.review-date-controls{
  display:grid !important;
  grid-template-columns:44px 150px 105px 44px auto;
  align-items:center;
  gap:7px;
}
.review-date-controls select,.review-date-controls button{
  height:42px;
}
.review-date-controls select{
  padding:8px 10px;border:1px solid #dbe3ea;border-radius:9px;background:#fff;font-weight:900
}

.review-summary-grid{
  display:grid;
  grid-template-columns:repeat(4,minmax(180px,1fr)) !important;
  gap:10px;
}
.rv-summary{min-height:102px;border:1px solid #dbe3ea;border-radius:14px;background:#fff;padding:13px;text-align:left;cursor:pointer}
.rv-summary span,.rv-summary small{display:block}.rv-summary span{font-size:10px;font-weight:900}.rv-summary b{display:block;font-size:23px;margin:7px 0}.rv-summary small{font-size:8px;color:#64748b}
.rv-summary.income{background:#ecfdf5;border-color:#86efac}
.rv-summary.expense{background:#fff1f2;border-color:#fda4af}
.rv-summary.saving{background:#eff6ff;border-color:#93c5fd}
.rv-summary.sleep{background:#f5f3ff;border-color:#c4b5fd}
.rv-summary.task{background:#f0fdf4;border-color:#86efac}
.rv-summary.pending{background:#fff7ed;border-color:#fdba74}
.rv-summary.calorie{background:#fffbeb;border-color:#fde68a}
.rv-summary.weight{background:#f8fafc;border-color:#cbd5e1}

.rv-calendar-head{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;margin-bottom:12px}
.rv-calendar-head h2{margin:0 0 4px}
.rv-calendar-head p{margin:0}
.rv-legend{display:flex;justify-content:flex-end;gap:7px;flex-wrap:wrap;font-size:8px;color:#64748b;max-width:620px}

.rv-week-head,.rv-calendar-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:7px}
.rv-week-head span{padding:8px;text-align:center;font-size:9px;font-weight:900;color:#64748b}
.rv-day{
  min-height:158px;border:1px solid #dfe6ee;border-radius:12px;background:#fff;padding:9px;cursor:pointer;overflow:hidden;
  transition:border .15s ease,box-shadow .15s ease,transform .15s ease
}
.rv-day:hover{border-color:#60a5fa;box-shadow:0 5px 16px rgba(15,23,42,.08);transform:translateY(-1px)}
.rv-day.today{outline:2px solid #2563eb;background:#eff6ff}
.rv-day.missing{background:#fffdf8}
.rv-day-num{font-weight:900;font-size:12px;margin-bottom:7px;display:flex;justify-content:space-between;align-items:center}
.rv-day-num small{font-size:7px;color:#f59e0b}
.rv-day-lines{display:flex;flex-direction:column;gap:4px;font-size:8px}
.rv-day-lines span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rv-day-lines .good{color:#15803d}.rv-day-lines .bad{color:#dc2626}.rv-day-lines .neutral{color:#475569}.rv-day-lines .pending{color:#b45309}
.rv-no-data{font-size:7.5px;color:#94a3b8;margin-top:8px}

.rv-trend-bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(27px,1fr));gap:4px;align-items:end;min-height:220px;padding:12px 4px}
.rv-trend-day{display:flex;flex-direction:column;align-items:center;gap:4px}
.rv-trend-stack{height:150px;width:100%;display:flex;align-items:end;justify-content:center;gap:2px}
.rv-trend-stack i{display:block;width:7px;border-radius:5px 5px 0 0}
.rv-trend-day small{font-size:7px;color:#64748b}

.rv-day-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px}
.rv-day-summary div{padding:11px;border:1px solid #e2e8f0;border-radius:10px;background:#f8fafc}
.rv-day-summary span,.rv-day-summary b{display:block}
.rv-day-summary span{font-size:8px;color:#64748b}.rv-day-summary b{font-size:16px;margin-top:4px}
.rv-day-task-list{margin-top:10px;border-top:1px solid #e2e8f0;padding-top:10px}
.rv-day-task-list h3{margin:0 0 7px}
.rv-day-task-row{display:grid;grid-template-columns:minmax(150px,1fr) 110px 90px;gap:8px;padding:7px 0;border-bottom:1px solid #eef2f7;align-items:center;font-size:9px}
.rv-day-task-row select{padding:6px;border:1px solid #dbe3ea;border-radius:7px}

.rv-quick-entry-wrap{margin-top:18px;padding-top:15px;border-top:2px solid #eef2f7}
.rv-quick-entry-wrap h3{margin:0 0 4px}
.rv-entry-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0}
.rv-entry-tabs button{padding:7px 10px;border:1px solid #dbe3ea;border-radius:999px;background:#f8fafc;font-size:8.5px;font-weight:900;cursor:pointer}
.rv-entry-tabs button.active{background:#0f172a;color:#fff;border-color:#0f172a}
.rv-entry-panel{display:none}
.rv-entry-panel.active{display:block}
.rv-entry-grid{display:grid;grid-template-columns:150px minmax(220px,1fr) 150px auto;gap:9px;align-items:end}
.rv-entry-grid.money{grid-template-columns:120px 150px 160px 150px minmax(220px,1fr) auto}
.rv-entry-grid.compact{grid-template-columns:180px 180px auto;max-width:650px}
.rv-entry-grid label{font-size:8.5px;font-weight:900;color:#475569}
.rv-entry-grid input,.rv-entry-grid select{display:block;width:100%;margin-top:4px;padding:8px;border:1px solid #cbd5e1;border-radius:8px;background:#fff}
.rv-day-modal-box{width:min(1250px,96vw);max-height:90vh;overflow:auto}

@media(max-width:1100px){
  .review-header{grid-template-columns:1fr !important}
  .review-date-controls{grid-template-columns:44px 1fr 110px 44px auto !important}
  .review-summary-grid{grid-template-columns:repeat(2,1fr)!important}
  .rv-entry-grid.money,.rv-entry-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:700px){
  .review-summary-grid{grid-template-columns:1fr!important}
  .review-date-controls{grid-template-columns:44px 1fr 90px 44px}
  .review-date-controls button:last-child{grid-column:1/-1}
  .rv-day{min-height:120px}
  .rv-entry-grid,.rv-entry-grid.money,.rv-entry-grid.compact{grid-template-columns:1fr}
}


/* ============================================================
   V100 REVIEW SYNC + METRIC FILTERS
   ============================================================ */
.review-date-controls{
  grid-template-columns:44px 150px 105px 44px auto auto minmax(120px,auto) !important;
}
.rv-sync-status{
  font-size:8px;
  font-weight:800;
  color:#64748b;
  white-space:nowrap;
}
.rv-sync-status.ok{color:#15803d}
.rv-sync-status.bad{color:#dc2626}
.rv-summary.active{
  outline:3px solid #0f172a;
  outline-offset:2px;
}
.rv-metric-filter{
  display:flex;
  align-items:center;
  gap:7px;
  flex-wrap:wrap;
  padding:12px 14px;
}
.rv-metric-filter>div{
  min-width:220px;
  margin-right:auto;
}
.rv-metric-filter>div b,.rv-metric-filter>div span{display:block}
.rv-metric-filter>div span{font-size:8px;color:#64748b;margin-top:2px}
.rv-metric-filter button{
  padding:7px 10px;
  border:1px solid #dbe3ea;
  border-radius:999px;
  background:#f8fafc;
  font-size:8px;
  font-weight:900;
  cursor:pointer;
}
.rv-metric-filter button.active{
  background:#0f172a;
  color:#fff;
  border-color:#0f172a;
}
.rv-day.metric-missing{
  background:#fff8f1;
  border-color:#fed7aa;
}
.rv-metric-missing-note{
  margin-top:8px;
  padding:5px 6px;
  border-radius:7px;
  background:#fff7ed;
  color:#b45309;
  font-size:7px;
  font-weight:800;
}
@media(max-width:1150px){
  .review-date-controls{grid-template-columns:44px 1fr 110px 44px auto auto !important}
  .rv-sync-status{grid-column:1/-1}
}


/* V101 review startup/sync robustness */
.rv-sync-status{min-width:150px}
.rv-sync-status.bad{color:#b45309 !important}

/* V102 Review calendar guaranteed layout */
#rvCalendarGrid{min-height:520px}
.rv-day-empty{visibility:hidden;min-height:150px}
.rv-sync-btn:disabled{opacity:.55;cursor:wait}

/* V103 full-sheet sync diagnostics */
.rv-sync-status.ok{font-weight:900}
.rv-sync-status.bad{font-weight:900}

/* ============================================================
   V106 STOCK PERFORMANCE SCANNER
   ============================================================ */
.stock-scanner-shell{max-width:1600px}
.stock-page-head{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:14px}
.stock-page-head h1{margin:0 0 5px}
.st-sync-card{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:14px}
.st-date-range{font-size:9px;font-weight:900;color:#334155}
.st-controls{margin-bottom:14px}
.st-period-buttons,.st-custom-controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.st-period-buttons button,.st-custom-controls button{
  border:1px solid #d7e0ea;background:#f8fafc;border-radius:999px;
  padding:9px 14px;font-weight:900;cursor:pointer
}
.st-period-buttons button.active,.st-custom-controls button.active{
  background:#0f172a;color:white;border-color:#0f172a
}
.st-custom-controls{margin-top:10px;padding-top:10px;border-top:1px solid #eef2f7;display:none}
.st-custom-controls.visible{display:flex}
.st-custom-controls span{font-size:9px;font-weight:900;color:#64748b;margin-right:4px}
.st-search-row{display:grid;grid-template-columns:minmax(240px,1fr) 260px;gap:10px;margin-top:12px}
.st-search-row input,.st-search-row select{
  width:100%;padding:10px 12px;border:1px solid #d7e0ea;border-radius:9px;background:white
}
.st-summary-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}
.st-summary{min-height:105px}
.st-summary span,.st-summary small{display:block}
.st-summary span{font-size:9px;font-weight:900;color:#64748b}
.st-summary b{display:block;font-size:23px;margin:8px 0}
.st-summary small{font-size:8px;color:#64748b}
.st-best{background:#ecfdf5;border-color:#86efac}
.st-worst{background:#fff1f2;border-color:#fda4af}
.st-table-card{padding:0;overflow:hidden}
.st-table-head{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;padding:16px 18px;border-bottom:1px solid #e2e8f0}
.st-table-head h2{margin:0 0 4px}
.st-table-actions{display:flex;gap:7px;flex-wrap:wrap}
.st-table-wrap{overflow:auto;max-height:70vh}
.st-table{width:100%;border-collapse:collapse;min-width:1180px}
.st-table th{
  position:sticky;top:0;z-index:2;background:#2563eb;color:white;
  padding:10px 9px;font-size:9px;text-align:right
}
.st-table th:nth-child(1),.st-table th:nth-child(2),.st-table th:nth-child(3){text-align:left}
.st-table td{padding:9px;border-bottom:1px solid #e5e7eb;font-size:9px;text-align:right;white-space:nowrap}
.st-table td:nth-child(1),.st-table td:nth-child(2),.st-table td:nth-child(3){text-align:left}
.st-table tr:hover td{background:#f8fafc}
.st-rank{font-weight:900}
.st-symbol{font-weight:900;color:#0f172a}
.st-ticker{font-size:7.5px;color:#64748b;margin-top:2px}
.st-positive{color:#15803d;font-weight:900}
.st-negative{color:#dc2626;font-weight:900}
.st-neutral{color:#475569;font-weight:900}
.st-value{
  display:inline-block;min-width:72px;padding:5px 8px;border-radius:999px;
  background:#f1f5f9;font-weight:900
}
.st-value.up{background:#dcfce7;color:#15803d}
.st-value.down{background:#fee2e2;color:#dc2626}
.st-empty{text-align:center!important;color:#64748b;padding:24px!important}
.st-insufficient{color:#94a3b8;font-style:italic}
@media(max-width:1000px){
  .st-summary-grid{grid-template-columns:repeat(2,1fr)}
  .stock-page-head{align-items:flex-start;flex-direction:column}
}
@media(max-width:700px){
  .st-summary-grid{grid-template-columns:1fr}
  .st-search-row{grid-template-columns:1fr}
}


/* ============================================================
   V107 STOCKS ICON HUB
   ============================================================ */
.stock-hub-shell{max-width:1600px}
.stock-hub-head{margin-bottom:14px}
.stock-hub-head h1{margin:0 0 5px}
.stock-tool-icons{
  display:grid;
  grid-template-columns:repeat(2,minmax(240px,320px));
  gap:12px;
  margin-bottom:16px
}
.stock-tool-card{
  display:flex;
  flex-direction:column;
  align-items:flex-start;
  min-height:115px;
  padding:17px;
  border:1px solid #dbe3ea;
  border-radius:15px;
  background:#fff;
  cursor:pointer;
  text-align:left;
  transition:.15s ease
}
.stock-tool-card:hover{border-color:#60a5fa;transform:translateY(-1px);box-shadow:0 6px 16px rgba(15,23,42,.06)}
.stock-tool-card.active{background:#eff6ff;border-color:#60a5fa;box-shadow:inset 0 0 0 1px #60a5fa}
.stock-tool-emoji{font-size:24px;margin-bottom:8px}
.stock-tool-card b{font-size:15px;margin-bottom:3px}
.stock-tool-card small{font-size:8px;color:#64748b}
.stock-tool-panel{display:none}
.stock-tool-panel.open{display:block}
.stock-tool-panel-head{
  display:flex;justify-content:space-between;align-items:flex-start;gap:12px;
  margin:10px 0 12px
}
.stock-tool-panel-head h2{margin:0 0 4px}
.stock-previous-placeholder{min-height:180px}
.stock-prev-note{
  margin-top:12px;padding:12px;border:1px solid #dbeafe;background:#eff6ff;
  border-radius:10px;color:#1e3a8a;font-size:9px
}
.st-sync-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:flex-end}
@media(max-width:700px){.stock-tool-icons{grid-template-columns:1fr}}

\n/* V108 STOCKS: single page scroll, compact full-width table */\n#stScannerTool .st-table-wrap{overflow:visible!important;max-height:none!important;height:auto!important}\n#stScannerTool .st-table-card{overflow:visible!important}\n#stScannerTool .st-table{width:100%!important;min-width:0!important;table-layout:fixed!important;font-size:8.5px!important}\n#stScannerTool .st-table th{position:sticky;top:0;z-index:3;padding:7px 3px!important;font-size:8px!important;line-height:1.05!important;white-space:normal!important}\n#stScannerTool .st-table td{padding:7px 3px!important;font-size:8.2px!important;line-height:1.15!important;white-space:normal!important;overflow:hidden;text-overflow:ellipsis;vertical-align:middle}\n#stScannerTool .st-table th:nth-child(1),#stScannerTool .st-table td:nth-child(1){width:4%}\n#stScannerTool .st-table th:nth-child(2),#stScannerTool .st-table td:nth-child(2){width:9%}\n#stScannerTool .st-table th:nth-child(3),#stScannerTool .st-table td:nth-child(3){width:18%}\n#stScannerTool .st-table th:nth-child(4),#stScannerTool .st-table td:nth-child(4){width:13%}\n#stScannerTool .st-table th:nth-child(5),#stScannerTool .st-table td:nth-child(5){width:8%}\n#stScannerTool .st-table th:nth-child(6),#stScannerTool .st-table td:nth-child(6){width:8%}\n#stScannerTool .st-table th:nth-child(7),#stScannerTool .st-table td:nth-child(7){width:8%}\n#stScannerTool .st-table th:nth-child(8),#stScannerTool .st-table td:nth-child(8){width:8%}\n#stScannerTool .st-table th:nth-child(9),#stScannerTool .st-table td:nth-child(9){width:8%}\n#stScannerTool .st-table th:nth-child(10),#stScannerTool .st-table td:nth-child(10){width:9%}\n#stScannerTool .st-table th:nth-child(11),#stScannerTool .st-table td:nth-child(11){width:7%}\n.st-search-row-v108{grid-template-columns:minmax(220px,1.5fr) minmax(140px,.8fr) minmax(130px,.7fr) minmax(160px,.9fr)!important}\n.st-period-date-strip{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:10px;padding:12px 14px!important;margin:10px 0!important}.st-period-date-strip>div{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:9px 11px}.st-period-date-strip span{display:block;font-size:7.5px;color:#64748b;font-weight:800;margin-bottom:4px}.st-period-date-strip b{font-size:11px}\n.st-sector-pill,.st-cap-pill{display:inline-block;max-width:100%;padding:3px 5px;border-radius:999px;background:#f1f5f9;color:#334155;font-size:7.3px;font-weight:800;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.st-trend-up{color:#15803d;font-weight:900}.st-trend-down{color:#dc2626;font-weight:900}.st-trend-flat{color:#64748b;font-weight:900}\n@media(max-width:1100px){.st-search-row-v108{grid-template-columns:1fr 1fr!important}}\n

/* ============================================================
   V109 MONEY — QUICK ENTRY + HELP SYNC
   ============================================================ */
.money-quick-entry-card{
  border:2px solid #bfdbfe;
  background:linear-gradient(135deg,#ffffff,#f8fbff);
  margin-top:12px!important;
}
.money-quick-entry-head{
  display:flex;
  justify-content:space-between;
  gap:14px;
  align-items:flex-start;
  margin-bottom:10px;
}
.money-quick-entry-head h2{margin:0 0 4px}
.money-quick-entry-actions{
  display:flex;
  gap:8px;
  align-items:center;
  flex-wrap:wrap;
  justify-content:flex-end;
}
#moneyQuickEntry .card{
  box-shadow:none!important;
  margin:0!important;
  padding:0!important;
  background:transparent!important;
}
#moneyQuickEntry .form-grid{
  grid-template-columns:1fr 1fr 1fr 1fr;
  gap:10px;
}
#moneyQuickEntry .money-quick-line{
  display:grid;
  grid-template-columns:1fr 1fr 1.4fr 1fr 1fr;
  gap:10px;
  align-items:end;
}
#moneyQuickEntry label{margin:4px 0}
#moneyQuickEntry .actions{margin-top:10px}
@media(max-width:1050px){
  #moneyQuickEntry .form-grid,
  #moneyQuickEntry .money-quick-line{grid-template-columns:1fr 1fr}
}
@media(max-width:650px){
  .money-quick-entry-head{flex-direction:column}
  #moneyQuickEntry .form-grid,
  #moneyQuickEntry .money-quick-line{grid-template-columns:1fr}
}


/* V112 — NSE PRO external Streamlit terminal */
.stock-tool-icons{grid-template-columns:repeat(4,minmax(210px,1fr))!important}
.stock-tool-nsepro{background:linear-gradient(135deg,#07111f,#10213a)!important;border-color:#1d4ed8!important;color:#fff!important}
.stock-tool-nsepro b{color:#fff!important}
.stock-tool-nsepro small{color:#bfdbfe!important;font-size:9px!important;line-height:1.35}
.stock-tool-nsepro:hover{border-color:#38bdf8!important;box-shadow:0 10px 24px rgba(37,99,235,.20)!important;transform:translateY(-2px)!important}
.stock-tool-nsepro .stock-tool-emoji{font-size:30px}
@media(max-width:1200px){.stock-tool-icons{grid-template-columns:repeat(2,minmax(220px,1fr))!important}}
@media(max-width:700px){.stock-tool-icons{grid-template-columns:1fr!important}}

/* ============================================================
   V110 PRO STOCK ANALYZER
   ============================================================ */
.stock-tool-icons{grid-template-columns:repeat(3,minmax(240px,320px))!important}
.stock-tool-pro{background:linear-gradient(135deg,#f8fafc,#eef2ff)}
.st-pro-panel-head{margin-top:8px}
.st-pro-head-actions{display:flex;gap:8px;flex-wrap:wrap}

.st-pro-grid{
  display:grid;
  grid-template-columns:290px minmax(0,1fr);
  gap:14px;
  align-items:start;
}
.st-pro-sidebar{
  position:sticky;
  top:12px;
  padding:14px!important;
  max-height:calc(100vh - 30px);
  overflow:auto;
}
.st-pro-side-section{padding:6px 0 14px;border-bottom:1px solid #e2e8f0;margin-bottom:10px}
.st-pro-side-section:last-child{border-bottom:0}
.st-pro-side-section h3{margin:0 0 9px;font-size:13px}
.st-pro-side-section input,.st-pro-side-section select{
  width:100%;padding:10px;border:1px solid #cbd5e1;border-radius:9px;background:#fff
}
.st-pro-side-section button{
  width:100%;padding:8px 10px;border:1px solid #dbe3ea;border-radius:9px;
  background:#f8fafc;text-align:left;font-weight:800;margin:4px 0;cursor:pointer
}
.stp-check{display:flex;gap:8px;align-items:center;font-size:9px;margin:8px 0}
.stp-matches{margin-top:8px;max-height:220px;overflow:auto}
.stp-match{
  padding:8px;border:1px solid #e2e8f0;border-radius:8px;margin:5px 0;cursor:pointer;background:#fff
}
.stp-match:hover{background:#eff6ff;border-color:#93c5fd}
.stp-match b{display:block;font-size:9px}.stp-match small{font-size:7px;color:#64748b}

.stp-empty-state{text-align:center;padding:80px 20px!important}
.stp-empty-icon{font-size:48px;margin-bottom:12px}
.stp-stock-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:12px}
.stp-symbol-line{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.stp-symbol-line h1{margin:0}
.stp-badge{display:inline-block;padding:5px 9px;border-radius:999px;background:#e2e8f0;font-size:8px;font-weight:900}
.stp-source{text-align:right;font-size:8px;color:#64748b}.stp-source span,.stp-source b{display:block}.stp-source b{font-size:10px;color:#0f172a;margin-top:3px}

.stp-kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px}
.stp-kpi{min-height:100px}
.stp-kpi span,.stp-kpi small{display:block}.stp-kpi span{font-size:8px;color:#64748b;font-weight:900}.stp-kpi b{display:block;font-size:22px;margin:8px 0}.stp-kpi small{font-size:8px}

.stp-chart-card{padding:14px!important;margin-bottom:12px}
.stp-card-head{display:flex;justify-content:space-between;gap:12px}
.stp-card-head h2{margin:0 0 4px}
.stp-chart-wrap{width:100%;height:390px;margin-top:10px}
#stpChart{width:100%;height:100%;display:block;background:linear-gradient(180deg,#0b1220,#111827);border-radius:12px}

.stp-signal-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
.stp-signal-card{min-height:290px;background:#0b1220!important;color:#f8fafc;border-color:#1f2937!important}
.stp-signal-title{font-size:18px;font-weight:900;margin-bottom:14px}.stp-signal-title span{font-size:10px;color:#94a3b8;margin-left:5px}
.stp-rec-badge{display:inline-block;padding:10px 16px;border-radius:9px;font-size:15px;font-weight:900;margin-bottom:12px}
.stp-rec-badge.buy{background:#16a34a;color:white}.stp-rec-badge.watch{background:#f59e0b;color:#111827}.stp-rec-badge.avoid{background:#dc2626;color:white}.stp-rec-badge.neutral{background:#475569;color:white}
.stp-rec-text{font-size:10px;line-height:1.5;margin-bottom:12px;color:#e2e8f0}
.stp-signal-card h3{font-size:11px;margin:12px 0 8px}
.stp-factor-list{display:flex;flex-direction:column;gap:8px}
.stp-factor{font-size:9px;line-height:1.4;padding:8px 10px;border-radius:8px;background:#111827;border:1px solid #263244}
.stp-factor.good{border-color:#14532d}.stp-factor.bad{border-color:#7f1d1d}.stp-factor.warn{border-color:#78350f}

.stp-indicator-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.stp-indicator span,.stp-indicator small{display:block}.stp-indicator span{font-size:8px;color:#64748b;font-weight:900}.stp-indicator b{display:block;font-size:16px;margin:7px 0}.stp-indicator small{font-size:8px}
.stp-good{color:#15803d!important}.stp-bad{color:#dc2626!important}.stp-warn{color:#b45309!important}

@media(max-width:1200px){
  .stock-tool-icons{grid-template-columns:repeat(2,minmax(220px,1fr))!important}
  .st-pro-grid{grid-template-columns:1fr}
  .st-pro-sidebar{position:static;max-height:none}
  .stp-kpi-grid,.stp-indicator-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:760px){
  .stock-tool-icons{grid-template-columns:1fr!important}
  .stp-signal-grid,.stp-kpi-grid,.stp-indicator-grid{grid-template-columns:1fr}
  .stp-chart-wrap{height:300px}
}


/* ============================================================
   V111 — INTERNET PRO STOCK ANALYZER
   ============================================================ */
.stp-v111-shell{
  background:#070b13!important;
  color:#f8fafc!important;
  padding:0!important;
  border-radius:20px;
  overflow:hidden;
}
.stp-v111-topbar{
  display:flex;justify-content:space-between;align-items:center;gap:18px;
  padding:22px 26px;border-bottom:1px solid #1e293b;
  background:linear-gradient(135deg,#0b1220,#101827);
}
.stp-v111-topbar h2{margin:3px 0 4px;font-size:25px}
.stp-v111-topbar p{margin:0;color:#94a3b8;font-size:11px}
.stp-v111-kicker{font-size:8px;font-weight:900;letter-spacing:1.7px;color:#60a5fa}
.stp-v111-top-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.stp-v111-top-actions button{
  padding:9px 12px;border-radius:9px;background:#172033;color:#e2e8f0;border:1px solid #334155;font-weight:800
}
.stp-v111-provider{font-size:9px;font-weight:900;color:#4ade80;padding:7px 10px;border:1px solid #14532d;border-radius:999px;background:#052e16}

.stp-v111-layout{display:grid;grid-template-columns:310px minmax(0,1fr);min-height:780px}
.stp-v111-sidebar{
  background:#f5f7fb;color:#0f172a;padding:18px;border-right:1px solid #dbe3ec;
}
.stp-v111-sidebar section{padding:8px 0 18px;border-bottom:1px solid #d8dee8;margin-bottom:13px}
.stp-v111-sidebar h3{margin:0 0 12px;font-size:13px}
.stp-v111-sidebar label{font-size:9px;color:#475569;margin:8px 0 5px}
.stp-v111-sidebar input,.stp-v111-sidebar select{
  width:100%;margin:0;padding:11px 12px;border:1px solid #cbd5e1;border-radius:10px;background:#fff
}
.stp-v111-searchbox{display:grid;grid-template-columns:1fr auto;gap:6px}
.stp-v111-searchbox button{
  border-radius:10px;padding:0 12px;background:#2563eb;color:#fff;font-weight:900
}
.stp-v111-check{display:flex!important;align-items:center;gap:8px;margin:9px 0!important;font-size:9px!important;color:#0f172a!important}
.stp-v111-check input{width:auto!important;margin:0!important}
.stp-v111-mini-feature{
  padding:8px 9px;border-radius:8px;background:#fff;border:1px solid #e2e8f0;margin:5px 0;font-size:8px;font-weight:800
}
.stp-v111-note{padding:11px;border-radius:10px;background:#e8eef8;color:#475569;font-size:8px;line-height:1.45}
.stp-v111-matches{margin-top:7px;display:flex;flex-direction:column;gap:5px}
.stp-v111-match{padding:8px 9px;background:#fff;border:1px solid #dbe3ec;border-radius:8px;cursor:pointer}
.stp-v111-match:hover{border-color:#60a5fa;background:#eff6ff}
.stp-v111-match b{font-size:9px;display:block}.stp-v111-match span{font-size:7px;color:#64748b}

.stp-v111-main{background:#070b13;padding:22px;min-width:0;position:relative}
.stp-v111-hero-empty{
  min-height:650px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
  background:radial-gradient(circle at 50% 30%,rgba(37,99,235,.16),transparent 38%)
}
.stp-v111-hero-empty>div:first-child{font-size:70px}
.stp-v111-hero-empty h1{font-size:32px;margin:12px 0 8px}
.stp-v111-hero-empty p{color:#94a3b8;max-width:620px;line-height:1.6}
.stp-v111-popular{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:18px}
.stp-v111-popular button{background:#172033;color:#dbeafe;border:1px solid #334155;padding:9px 14px;border-radius:999px;font-weight:900}

.stp-v111-loader{
  position:absolute;inset:22px;z-index:20;background:rgba(7,11,19,.94);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;border-radius:16px
}
.stp-v111-loader span{font-size:9px;color:#94a3b8}
.stp-v111-spinner{width:44px;height:44px;border:4px solid #1e293b;border-top-color:#3b82f6;border-radius:50%;animation:stpSpin .8s linear infinite}
@keyframes stpSpin{to{transform:rotate(360deg)}}

.stp-v111-stock-header{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;margin-bottom:13px}
.stp-v111-symbol-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.stp-v111-symbol-row h1{margin:0;font-size:31px}
.stp-v111-chip{padding:5px 9px;border-radius:999px;background:#172033;border:1px solid #334155;color:#cbd5e1;font-size:8px;font-weight:900}
.stp-v111-live{color:#4ade80;border-color:#14532d;background:#052e16}
.stp-v111-subtitle{font-size:9px;color:#94a3b8;margin-top:4px}
.stp-v111-lastupdate{text-align:right}.stp-v111-lastupdate span{display:block;color:#64748b;font-size:8px}.stp-v111-lastupdate b{font-size:10px}

.stp-v111-kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:13px}
.stp-v111-kpi{
  padding:15px 16px;border-radius:14px;background:linear-gradient(145deg,#0d1421,#111a29);
  border:1px solid #1e293b;min-height:105px
}
.stp-v111-kpi span,.stp-v111-kpi small{display:block}.stp-v111-kpi span{font-size:7.5px;text-transform:uppercase;letter-spacing:.5px;color:#64748b;font-weight:900}
.stp-v111-kpi b{display:block;font-size:21px;margin:10px 0 5px}.stp-v111-kpi small{font-size:8px;color:#94a3b8}

.stp-v111-chart-card,.stp-v111-signal-card,.stp-v111-risk-card,.stp-v111-tech-card{
  background:#0b1019;border:1px solid #1e293b;border-radius:15px
}
.stp-v111-chart-card{padding:15px;margin-bottom:13px}
.stp-v111-chart-head{display:flex;justify-content:space-between;gap:12px;align-items:center}
.stp-v111-chart-head h2{margin:0 0 4px;font-size:17px}.stp-v111-chart-head p{margin:0;color:#64748b;font-size:8px}
.stp-v111-legend{display:flex;gap:10px;flex-wrap:wrap;font-size:7px;color:#94a3b8}
.stp-v111-legend span{display:flex;align-items:center;gap:4px}.stp-v111-legend i{width:16px;height:2px;display:block}
.stp-v111-legend i.price{background:#60a5fa}.stp-v111-legend i.sma20{background:#f59e0b}.stp-v111-legend i.sma50{background:#a78bfa}.stp-v111-legend i.ema9{background:#22c55e}
#stpChart{display:block;width:100%;height:430px;margin-top:12px;border-radius:12px;background:#080d16}

.stp-v111-signal-grid{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:13px}
.stp-v111-signal-card{padding:22px;min-height:350px}
.stp-v111-signal-heading{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}.stp-v111-signal-heading h2{margin:0;font-size:20px}.stp-v111-signal-heading span{font-size:8px;color:#64748b}
.stp-v111-rec{display:inline-block;margin:18px 0 12px;padding:10px 16px;border-radius:9px;font-weight:900;font-size:14px;background:#334155}
.stp-v111-rec.buy{background:#16a34a;color:white}.stp-v111-rec.strong{background:#00c853;color:white}.stp-v111-rec.watch{background:#f59e0b;color:#111827}.stp-v111-rec.avoid{background:#dc2626;color:white}.stp-v111-rec.neutral{background:#475569;color:white}
.stp-v111-signal-card p{font-size:9px;color:#d7dee9;line-height:1.55}.stp-v111-signal-card h3{font-size:10px;margin:15px 0 8px}
.stp-v111-factors{display:flex;flex-direction:column;gap:7px}
.stp-v111-factor{padding:8px 10px;border-radius:8px;background:#0f1724;border-left:3px solid #475569;font-size:8px;line-height:1.45}
.stp-v111-factor.good{border-left-color:#22c55e}.stp-v111-factor.bad{border-left-color:#ef4444}.stp-v111-factor.warn{border-left-color:#f59e0b}

.stp-v111-risk-card,.stp-v111-tech-card{padding:20px;margin-bottom:13px}
.stp-v111-section-title{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:16px}
.stp-v111-section-title h2{margin:0;font-size:18px}.stp-v111-section-title span{font-size:8px;color:#64748b}
.stp-v111-risk-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}
.stp-v111-risk-grid>div,.stp-v111-indicator-grid>div{
  padding:13px;border-radius:11px;background:#0e1623;border:1px solid #1f2937
}
.stp-v111-risk-grid span,.stp-v111-risk-grid small,.stp-v111-indicator-grid span,.stp-v111-indicator-grid small{display:block}
.stp-v111-risk-grid span,.stp-v111-indicator-grid span{font-size:7.5px;color:#64748b;font-weight:900}
.stp-v111-risk-grid b{display:block;font-size:19px;margin:8px 0}.stp-v111-risk-grid small{font-size:8px;color:#94a3b8}
.stp-v111-indicator-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}
.stp-v111-indicator-grid b{display:block;font-size:15px;margin:7px 0}.stp-v111-indicator-grid small{font-size:7.5px;color:#94a3b8}
.stp-v111-disclaimer{padding:10px 13px;border:1px solid #78350f;background:#1f1508;color:#fbbf24;border-radius:10px;font-size:7.5px;text-align:center}
.stp-pos{color:#4ade80!important}.stp-neg{color:#fb7185!important}.stp-warn-text{color:#fbbf24!important}

@media(max-width:1250px){
  .stp-v111-layout{grid-template-columns:260px minmax(0,1fr)}
  .stp-v111-kpis{grid-template-columns:repeat(3,1fr)}
  .stp-v111-risk-grid{grid-template-columns:repeat(3,1fr)}
  .stp-v111-indicator-grid{grid-template-columns:repeat(3,1fr)}
}
@media(max-width:900px){
  .stp-v111-layout{grid-template-columns:1fr}
  .stp-v111-sidebar{border-right:0;border-bottom:1px solid #dbe3ec}
  .stp-v111-signal-grid{grid-template-columns:1fr}
  .stp-v111-kpis{grid-template-columns:repeat(2,1fr)}
  .stp-v111-risk-grid,.stp-v111-indicator-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:600px){
  .stp-v111-topbar,.stp-v111-stock-header,.stp-v111-section-title{flex-direction:column}
  .stp-v111-kpis,.stp-v111-risk-grid,.stp-v111-indicator-grid{grid-template-columns:1fr}
  #stpChart{height:320px}
}


.bank-centered-table{
  width:100%;
  table-layout:auto;
}
.bank-centered-table th,
.bank-centered-table td{
  text-align:center !important;
  vertical-align:middle !important;
}
.bank-centered-table th:nth-child(6),
.bank-centered-table th:nth-child(7),
.bank-centered-table th:nth-child(8),
.bank-centered-table td:nth-child(6),
.bank-centered-table td:nth-child(7),
.bank-centered-table td:nth-child(8){
  text-align:center !important;
}

/* V160 — Money Insights */
.mi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:14px 0}
.mi-card{border:1px solid #dbe3ef;border-radius:16px;padding:16px;background:#fff;min-width:0}
.mi-card span{display:block;color:#64748b;font-size:13px;margin-bottom:6px}.mi-card b{font-size:24px;line-height:1.15;overflow-wrap:anywhere}.mi-card small{display:block;color:#64748b;margin-top:6px}
.mi-good b{color:#15803d}.mi-warn b{color:#c2410c}.mi-blue b{color:#2563eb}.mi-purple b{color:#7c3aed}
.mi-section{border:1px solid #dbe3ef;border-radius:16px;padding:16px;background:#fff;margin-top:14px}.mi-section h3{margin:0 0 12px}.mi-row{display:grid;grid-template-columns:minmax(130px,1.5fr) minmax(90px,.8fr) minmax(90px,.8fr) minmax(90px,.8fr);gap:10px;align-items:center;padding:10px 0;border-bottom:1px solid #eef2f7}.mi-row:last-child{border-bottom:0}.mi-row input{width:100%;box-sizing:border-box;padding:9px 10px;border:1px solid #cbd5e1;border-radius:9px;font-size:15px}.mi-bar{height:8px;background:#eef2f7;border-radius:99px;overflow:hidden;margin-top:6px}.mi-bar span{display:block;height:100%;background:#64748b;border-radius:99px}.mi-insight{padding:11px 12px;border-radius:12px;background:#f8fafc;border:1px solid #e2e8f0;margin:8px 0}.mi-insight strong{display:block;margin-bottom:3px}.mi-positive{color:#15803d}.mi-negative{color:#dc2626}.mi-neutral{color:#334155}.mi-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.mi-actions button{min-height:42px}.mi-subgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.mi-empty{color:#64748b;padding:12px 0}
@media(max-width:900px){.mi-grid{grid-template-columns:1fr 1fr}.mi-subgrid{grid-template-columns:1fr}}
@media(max-width:560px){.mi-grid{grid-template-columns:1fr}.mi-row{grid-template-columns:1fr 1fr}.mi-row>*:first-child{grid-column:1/-1}}

.mi-forecast-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:12px 0}.mi-forecast-grid>div{padding:12px;border:1px solid #e2e8f0;border-radius:12px;background:#f8fafc}.mi-forecast-grid span{display:block;color:#64748b;font-size:12px}.mi-forecast-grid b{display:block;margin-top:5px;font-size:18px}.mi-safe-result{border-width:2px!important}.mi-safe-result b{color:#15803d;font-size:22px}.mi-commit-form{display:grid;grid-template-columns:150px minmax(160px,1fr) 150px auto;gap:10px;align-items:end}.mi-commit-form input{width:100%;box-sizing:border-box;padding:10px;border:1px solid #cbd5e1;border-radius:9px;font-size:15px}.mi-commit-row{display:grid;grid-template-columns:1fr auto auto;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid #eef2f7}.mi-commit-row small{display:block;color:#64748b;margin-top:3px}@media(max-width:700px){.mi-forecast-grid{grid-template-columns:1fr 1fr}.mi-commit-form{grid-template-columns:1fr 1fr}.mi-commit-form button{grid-column:1/-1}}@media(max-width:480px){.mi-forecast-grid,.mi-commit-form{grid-template-columns:1fr}.mi-commit-row{grid-template-columns:1fr auto}}

/* V163 — Room Option 3: Family Private Ledger */
.private-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.private-tab{border:0;border-radius:999px;padding:9px 16px;font-weight:800;cursor:pointer;background:#e2e8f0;color:#0f172a}.private-tab.active{background:#7c3aed;color:#fff}.private-grid{display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:10px;margin:12px 0}.private-card{padding:14px;border:1px solid #e2e8f0;border-radius:14px;background:#fff}.private-card span{display:block;font-size:11px;color:#64748b;font-weight:800}.private-card b{display:block;font-size:20px;margin-top:5px}.private-panel{padding:16px;border:1px solid #e2e8f0;border-radius:16px;background:#fff;margin:14px 0}.private-form{display:flex;gap:8px;flex-wrap:wrap;align-items:end}.private-form label{font-size:11px;font-weight:800;color:#475569}.private-form input,.private-form select{display:block;margin-top:4px;padding:9px 10px;border:1px solid #cbd5e1;border-radius:9px;background:#fff}.private-good{color:#15803d}.private-warn{color:#b45309}.private-secret{color:#7c3aed}.private-table{overflow:auto;margin-top:12px}.private-table table{width:100%;border-collapse:collapse;font-size:12px}.private-table th,.private-table td{padding:9px;border-bottom:1px solid #e5e7eb;text-align:left}.private-table th{background:#f8fafc;position:sticky;top:0}@media(max-width:850px){.private-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:550px){.private-grid{grid-template-columns:1fr}}

/* V163 - compact visual insights: keep the ordered cards readable on wide screens */
#money .money-insights-heading,
#money .money-chart-card{
  width:min(1120px,calc(100% - 20px));
  margin-left:auto;
  margin-right:auto;
}
#money .money-chart-card{
  padding:12px 14px;
  border-radius:15px;
  margin-bottom:10px;
}
#money .money-card-title-row{margin-bottom:7px}
#money .money-card-title-row h3{font-size:16px}
#money .money-card-title-row p{font-size:10px}
#money .money-svg-chart{height:220px}
#money .money-empty-chart{height:180px}
#money .money-donut-layout{grid-template-columns:145px 1fr;gap:12px}
#money .money-donut{width:140px;height:140px}
#money .money-donut:after{width:88px;height:88px}
#money .money-progress-list{gap:9px}
#money .money-all-category-chart{font-size:11px}
@media(max-width:700px){
  #money .money-insights-heading,
  #money .money-chart-card{width:100%}
  #money .money-svg-chart{height:205px}
  #money .money-donut-layout{grid-template-columns:1fr;justify-items:center}
}

</style>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

<style>
/* V113 — Bank Wise Money View */
.bank-wise-summary{
  display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));
  gap:12px;margin:14px 0;
}
.bank-wise-kpi{
  padding:16px;border-radius:14px;border:1px solid #dbeafe;background:#f8fbff;
}
.bank-wise-kpi span{display:block;font-size:11px;color:#64748b;font-weight:700}
.bank-wise-kpi b{display:block;margin-top:6px;font-size:22px;color:#0f172a}
.bank-account-grid{
  display:grid;grid-template-columns:repeat(4,minmax(160px,1fr));
  gap:10px;margin:14px 0;
}
.bank-account-card{
  text-align:left;padding:14px;border:1px solid #cbd5e1;border-radius:12px;
  background:#fff;cursor:pointer;transition:.15s ease;
}
.bank-account-card:hover,.bank-account-card.active{
  border-color:#2563eb;background:#eff6ff;transform:translateY(-1px);
}
.bank-account-card b{display:block;color:#0f172a}
.bank-account-card span{display:block;color:#64748b;font-size:11px;margin-top:4px}
.bank-saving-chip{
  display:inline-flex;gap:6px;align-items:center;margin:4px 6px 4px 0;
  padding:7px 10px;border-radius:999px;background:#eef2ff;color:#3730a3;
  font-size:11px;font-weight:700;
}
.bank-tx-table{overflow:auto;margin-top:12px}
.bank-tx-table table{width:100%;border-collapse:collapse;font-size:12px}
.bank-tx-table th,.bank-tx-table td{padding:8px;border-bottom:1px solid #e5e7eb;text-align:left}
.bank-tx-table th{background:#f8fafc;position:sticky;top:0}
@media(max-width:1000px){
  .bank-wise-summary,.bank-account-grid{grid-template-columns:repeat(2,minmax(150px,1fr))}
}
@media(max-width:650px){
  .bank-wise-summary,.bank-account-grid{grid-template-columns:1fr}
}
</style>


<style>
/* V114 — Bank Wise Quick Entry */
.bank-quick-entry{
  margin:14px 0 16px;padding:16px;border:1px solid #bfdbfe;border-radius:14px;
  background:linear-gradient(135deg,#f8fbff,#eff6ff);
}
.bank-quick-entry-head{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:10px}
.bank-quick-entry-head h3{margin:0}
.bank-quick-grid{
  display:grid;grid-template-columns:1fr .8fr 1fr 1fr;gap:10px;align-items:end;
}
.bank-quick-line{
  display:grid;grid-template-columns:1.5fr 1fr auto;gap:10px;align-items:end;margin-top:10px;
}
.bank-quick-entry label{font-size:12px;font-weight:700;color:#334155}
.bank-quick-entry input,.bank-quick-entry select{
  width:100%;margin-top:5px;box-sizing:border-box;
}
@media(max-width:950px){
 .bank-quick-grid{grid-template-columns:1fr 1fr}
 .bank-quick-line{grid-template-columns:1fr 1fr}
}
@media(max-width:600px){
 .bank-quick-grid,.bank-quick-line{grid-template-columns:1fr}
}
</style>


<style>
.mt-dashboard-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.mt-dashboard-grid .tile{min-height:145px}
.mt-notes-tile{background:linear-gradient(135deg,#fff7ed,#fffbeb)!important;border:1px solid #fdba74!important}
.mt-notes-head{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:16px}
.mt-note-form{display:grid;grid-template-columns:1fr 2fr 1.4fr 1fr;gap:12px;margin-bottom:12px}
.mt-note-editor label{display:flex;flex-direction:column;gap:6px;font-weight:700}
.mt-note-editor input,.mt-note-editor select,.mt-note-editor textarea,.mt-notes-toolbar input,.mt-notes-toolbar select{
  width:100%;box-sizing:border-box;border:1px solid #cbd5e1;border-radius:10px;padding:11px 12px;background:#fff;color:#0f172a
}
.mt-note-editor textarea{resize:vertical;line-height:1.5}
.mt-note-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:12px}
.mt-notes-toolbar{display:grid;grid-template-columns:1fr minmax(260px,1.2fr) minmax(180px,.6fr);gap:12px;align-items:center;margin-bottom:16px}
.mt-notes-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.mt-note-card{border:1px solid #dbe3ef;border-radius:14px;padding:16px;background:#fff;box-shadow:0 3px 12px rgba(15,23,42,.04)}
.mt-note-card-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
.mt-note-card h3{margin:0 0 5px;font-size:18px}
.mt-note-meta{font-size:12px;color:#64748b}
.mt-note-body{white-space:pre-wrap;line-height:1.5;margin:12px 0;color:#334155;max-height:180px;overflow:auto}
.mt-note-card-actions{display:flex;gap:8px}
.mt-note-card-actions button{padding:7px 10px;border-radius:8px;font-size:12px}
.mt-note-tag{display:inline-block;padding:4px 8px;border-radius:999px;background:#eef2ff;color:#4338ca;font-size:11px;font-weight:800;margin-right:6px}
@media(max-width:1000px){.mt-dashboard-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.mt-note-form{grid-template-columns:1fr 1fr}.mt-notes-list{grid-template-columns:1fr}}
@media(max-width:700px){.mt-dashboard-grid,.mt-note-form,.mt-notes-toolbar{grid-template-columns:1fr}.mt-notes-head{align-items:flex-start;flex-direction:column}}
</style>


<style>
/* V156 — Room home: Sharing + Gifts */
.room-mode-grid{display:grid;grid-template-columns:repeat(2,minmax(220px,1fr));gap:14px;margin:16px 0}
.room-mode-card{padding:22px;border:1px solid #cbd5e1;border-radius:16px;background:#fff;cursor:pointer;text-align:left}
.room-mode-card:hover{border-color:#7c3aed;background:#f5f3ff}
.room-mode-card .ico{font-size:34px;display:block;margin-bottom:8px}
.room-mode-card b{display:block;font-size:18px;color:#0f172a}
.room-mode-card span{display:block;margin-top:6px;color:#64748b;font-size:12px;line-height:1.45}
.gift-red{color:#dc2626!important;font-weight:900}
.gift-green{color:#15803d!important;font-weight:900}
.gift-zero{color:#475569!important;font-weight:900}
@media(max-width:650px){.room-mode-grid{grid-template-columns:1fr}}

/* V156 — Room / Shared Expense Ledger */
.room-top{display:grid;grid-template-columns:repeat(3,minmax(150px,1fr));gap:12px;margin:14px 0}
.room-kpi{padding:16px;border:1px solid #e2e8f0;border-radius:14px;background:#fff}
.room-kpi span{display:block;color:#64748b;font-size:11px;font-weight:800}
.room-kpi b{display:block;font-size:22px;margin-top:6px;color:#0f172a}
.room-person-grid{display:grid;grid-template-columns:repeat(4,minmax(160px,1fr));gap:10px;margin:14px 0}
.room-person-card{text-align:left;padding:14px;border:1px solid #cbd5e1;border-radius:13px;background:#fff;cursor:pointer}
.room-person-card.active,.room-person-card:hover{border-color:#7c3aed;background:#f5f3ff}
.room-person-card b{display:block;font-size:15px;color:#0f172a}
.room-person-card span{display:block;margin-top:5px;font-size:11px;color:#64748b}
.room-status-owe{color:#b45309!important;font-weight:900}
.room-status-settled{color:#15803d!important;font-weight:900}
.room-table{overflow:auto;margin-top:12px}
.room-table table{width:100%;border-collapse:collapse;font-size:12px}
.room-table th,.room-table td{padding:9px;border-bottom:1px solid #e5e7eb;text-align:left}
.room-table th{background:#f8fafc;position:sticky;top:0}
.room-split-note{padding:10px 12px;border-radius:10px;background:#f5f3ff;color:#5b21b6;font-size:12px;margin:10px 0}
@media(max-width:1000px){.room-person-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:650px){.room-top,.room-person-grid{grid-template-columns:1fr}}

/* V156: no-JavaScript fallback for START TRACKING */
#app:target{display:block!important}
body:has(#app:target) #welcome{display:none!important}


/* ===== Journal Habit Tracker — monthly dot grid ===== */
.jh-wrap{overflow-x:auto;padding:4px 0 10px}
.jh-table{border-collapse:separate;border-spacing:0 7px;min-width:980px;width:100%}
.jh-table th{font-size:11px;color:#64748b;font-weight:800;text-align:center;white-space:nowrap}
.jh-table th.jh-name{text-align:left;min-width:190px;position:sticky;left:0;background:#fff;z-index:3}
.jh-table td{padding:0 2px;text-align:center}
.jh-table td.jh-name{position:sticky;left:0;background:#fff;z-index:2;text-align:left;padding-right:14px;min-width:190px}
.jh-habit-title{font-weight:800;color:#1e293b;white-space:nowrap}
.jh-habit-meta{font-size:11px;color:#94a3b8;margin-top:2px}
.jh-dot{appearance:none;-webkit-appearance:none;width:17px;height:17px;border:1.8px solid #94a3b8;border-radius:50%;background:#fff;cursor:pointer;margin:0;vertical-align:middle;transition:.12s}
.jh-dot:hover{transform:scale(1.18);border-color:#2563eb}
.jh-dot:checked{background:#22c55e;border-color:#16a34a;box-shadow:inset 0 0 0 3px #dcfce7}
.jh-dot.jh-off{opacity:.16;cursor:default;background:#e2e8f0;border-color:#cbd5e1}
.jh-today{background:#eff6ff!important;border-radius:6px}
.jh-stamp{font-size:10px;color:#64748b;white-space:nowrap;display:block;margin-top:2px;min-height:12px}
.jh-progress{font-size:12px;font-weight:800;color:#475569;white-space:nowrap}


.hb-wrap{overflow-x:auto;padding-bottom:10px}.hb-table{border-collapse:separate;border-spacing:0 7px;min-width:1050px;width:100%}
.hb-table th{font-size:11px;color:#64748b;text-align:center}.hb-table th:first-child,.hb-table td:first-child{position:sticky;left:0;background:#fff;z-index:2;text-align:left;min-width:215px}
.hb-table td{text-align:center;padding:0 2px}.hb-dot{appearance:none;-webkit-appearance:none;width:19px;height:19px;border:2px solid #94a3b8;border-radius:50%;background:#fff;cursor:pointer;margin:0}
.hb-dot:checked{background:#22c55e;border-color:#16a34a;box-shadow:inset 0 0 0 3px #dcfce7}.hb-dot.hb-off{opacity:.12;cursor:default;background:#e2e8f0}
.hb-name{font-weight:800}.hb-meta{font-size:11px;color:#94a3b8;margin-top:2px}.hb-actions{display:flex;gap:5px;margin-top:5px}.hb-actions button{padding:4px 7px;font-size:11px}.hb-today{background:#eff6ff!important;border-radius:7px}

/* ===== Schedule ===== */
.sc-day-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}
.sc-timeline{display:grid;grid-template-columns:105px 1fr;border:1px solid #e2e8f0;border-radius:14px;overflow:hidden}
.sc-time{padding:12px 10px;border-bottom:1px solid #e2e8f0;background:#f8fafc;font-size:12px;font-weight:700;color:#64748b}
.sc-slot{min-height:48px;padding:5px 8px;border-bottom:1px solid #e2e8f0;cursor:pointer}
.sc-slot:hover{background:#f8fafc}
.sc-event{padding:8px 10px;border-radius:9px;background:#e0e7ff;border-left:4px solid #6366f1;margin:2px 0;cursor:pointer}
.sc-event b{display:block}.sc-event small{color:#64748b}
.sc-week{overflow:auto}.sc-week-table{width:100%;min-width:900px;border-collapse:collapse}
.sc-week-table th,.sc-week-table td{border:1px solid #dbe3ef;padding:8px;vertical-align:top}
.sc-week-table th{background:#eef2ff}.sc-week-time{white-space:nowrap;font-size:12px;color:#64748b;background:#f8fafc}
.sc-mini-event{padding:5px 6px;border-radius:6px;background:#fce7f3;margin:3px 0;font-size:12px;cursor:pointer}
.sc-month-grid{display:grid;grid-template-columns:repeat(7,minmax(120px,1fr));gap:1px;background:#dbe3ef;border:1px solid #dbe3ef;overflow:auto}
.sc-month-cell{background:#fff;min-height:115px;padding:7px}.sc-month-cell.sc-muted{background:#f8fafc;color:#94a3b8}
.sc-month-num{font-weight:800;margin-bottom:5px}.sc-month-event{font-size:11px;padding:4px 5px;background:#dcfce7;border-radius:5px;margin:3px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}
@media(max-width:800px){.sc-month-grid{grid-template-columns:repeat(7,minmax(95px,1fr))}.sc-timeline{grid-template-columns:82px 1fr}}

.sc-dual-head{display:grid;grid-template-columns:105px 1fr 1fr;background:#f8fafc;border:1px solid #e2e8f0;border-bottom:0;border-radius:14px 14px 0 0;overflow:hidden}
.sc-dual-head>div{padding:10px 12px;font-weight:800}.sc-dual-head>div+div{border-left:1px solid #e2e8f0}
.sc-dual{display:grid;grid-template-columns:105px 1fr 1fr;border:1px solid #e2e8f0;border-radius:0 0 14px 14px;overflow:hidden}
.sc-dual .sc-time,.sc-dual .sc-slot{border-bottom:1px solid #e2e8f0}.sc-dual .sc-actual{border-left:1px solid #e2e8f0;background:#fffdf7}
.sc-actual-event{padding:8px 10px;border-radius:9px;background:#dcfce7;border-left:4px solid #22c55e;margin:2px 0;cursor:pointer}
.sc-wake-banner{padding:10px 12px;border-radius:10px;background:#fff7ed;border:1px solid #fed7aa;margin-bottom:12px;font-weight:800}
@media(max-width:800px){.sc-dual-head,.sc-dual{grid-template-columns:82px minmax(230px,1fr) minmax(230px,1fr);min-width:560px}.sc-dual-wrap{overflow-x:auto}}
.sc-direct-cell{display:flex;gap:6px;align-items:center;width:100%}.sc-direct-input{width:100%;min-height:34px;border:1px solid transparent;background:transparent;border-radius:7px;padding:6px 8px;font:inherit;color:inherit;outline:none}.sc-direct-input:hover{border-color:#cbd5e1;background:#fff}.sc-direct-input:focus{border-color:#60a5fa;background:#fff;box-shadow:0 0 0 2px rgba(96,165,250,.14)}.sc-direct-plan{background:#f8fbff}.sc-direct-actual{background:#fffdf7}.sc-direct-saved{font-size:10px;color:#16a34a;white-space:nowrap;opacity:0}.sc-direct-saved.show{opacity:1}</style>

</head>
<body>
<div id="masterBuildBadge" style="position:fixed;right:10px;bottom:10px;z-index:99999;background:#111827;color:white;padding:7px 10px;border-radius:8px;font:700 11px Arial;box-shadow:0 2px 8px #0003">
V159 · LOAN OUTSTANDING FIX
</div>


<div id="welcome" class="welcome visual-welcome">
  <div class="visual-landing-shell">
    <section class="visual-copy-panel">
      <div class="visual-eyebrow">YOUR PERSONAL DASHBOARD</div>
      <h1>My Tracking</h1>
      <p class="visual-lead">Track the life you are building — not just the days that pass.</p>

      <blockquote class="visual-quote">
        “Small things become powerful when you measure them consistently.”
      </blockquote>

      <div class="visual-topics">
        <span>Money</span><i></i><span>Health</span><i></i><span>Job</span><i></i><span>Productivity</span><i></i><span>Efficiency</span>
      </div>

      <div class="visual-actions">
        <a class="visual-start" href="#app" onclick="try{startApp()}catch(e){}" style="display:inline-flex;align-items:center;justify-content:center;text-decoration:none">START TRACKING</a>
        <div class="visual-hint">Your money, goals, work and daily progress — together.</div>
      </div>
    </section>

    <section class="visual-art-panel saree-hero-panel" aria-label="Nature landscape for My Tracking">
      <img class="tracking-hero-photo" src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1800&q=88" alt="Peaceful mountain lake and nature landscape">
      <div class="hero-glow hero-glow-one"></div>
      <div class="hero-glow hero-glow-two"></div>
      <div class="visual-art-caption">
        <span>MY TRACKING</span>
        <b>Plan better • Live better</b>
      </div>
      <div class="hero-quote-chip">“Your future is created by what you do today.”</div>
    </section>
  </div>
</div>

<div id="app" class="app">
<aside class="sidebar">
  <div class="brand">🌱 <span>My Tracking</span></div>
  <button class="nav active" onclick="showPage('dashboard',this)">🏠 <span>Dashboard</span></button>
  <button class="nav" onclick="showPage('money',this)">💰 <span>Money</span></button>
  <button class="nav" onclick="showPage('stocks',this)">📈 <span>Stocks</span></button>
  <button class="nav" onclick="showPage('time',this)">⏱️ <span>Time</span></button>
  <button class="nav" onclick="showPage('health',this)">❤️ <span>Health</span></button>
<button class="nav" onclick="showPage('mind',this)">🧠 <span>Mind</span></button>
  <button class="nav" onclick="showPage('learning',this)">📚 <span>Learning</span></button>
<button class="nav" onclick="showPage('tasks',this)">✅ <span>Tasks</span></button>
  <button class="nav" onclick="showPage('goals',this)">🎯 <span>Goals</span></button>
  <button class="nav" onclick="showPage('analytics',this)">📊 <span>Analytics</span></button>
  <div class="side-bottom">
      <button class="nav" onclick="showPage('review',this)">📔 <span>Journal</span></button>
<button class="nav" onclick="showPage('schedule',this);setTimeout(SC_render,0)">🗓️ <span>Schedule</span></button>
<button class="nav" onclick="showPage('habits',this);setTimeout(HB_renderAll,0)">🔁 <span>Habits</span></button>
<button class="nav" onclick="showPage('notes',this)">📝 <span>Notes</span></button>
<button class="nav" onclick="showPage('settings',this)">⚙️ <span>Settings</span></button></div>
</aside>

<main class="main">

<section id="dashboard" class="page active">
<div class="inner">
  <h1>🏠 Dashboard</h1>
  <div class="card">
    <h2>Welcome</h2>
    <p class="muted">Everything in My Tracking is available here. Click any card to open it.</p>
  </div>

  <div class="grid mt-dashboard-grid">
    <button class="tile" onclick="MT_openPage('money')"><div class="tile-icon">💰</div><b>Money</b><span class="muted">Income, expenses, savings, loans and bank view</span></button>
    <button class="tile" onclick="MT_openPage('stocks')"><div class="tile-icon">📈</div><b>Stocks</b><span class="muted">Stock performance and market tools</span></button>
    <button class="tile" onclick="MT_openPage('time')"><div class="tile-icon">⏱️</div><b>Time</b><span class="muted">Plan and track your complete day</span></button>
    <button class="tile" onclick="MT_openPage('health')"><div class="tile-icon">❤️</div><b>Health</b><span class="muted">Sleep, food, weight and wellness</span></button>
    <button class="tile" onclick="MT_openPage('mind')"><div class="tile-icon">🧠</div><b>Mind</b><span class="muted">Mind and personal reflection</span></button>
    <button class="tile" onclick="MT_openPage('learning')"><div class="tile-icon">📚</div><b>Learning</b><span class="muted">Learning tracker and study notes</span></button>
    <button class="tile" onclick="MT_openPage('tasks')"><div class="tile-icon">✅</div><b>Tasks</b><span class="muted">Tasks, status and progress</span></button>
    <button class="tile" onclick="MT_openPage('goals')"><div class="tile-icon">🎯</div><b>Goals</b><span class="muted">Goals and milestones</span></button>
    <button class="tile" onclick="MT_openPage('analytics')"><div class="tile-icon">📊</div><b>Analytics</b><span class="muted">See your tracking analytics</span></button>
    <button class="tile" onclick="MT_openPage('review')"><div class="tile-icon">🗓️</div><b>Journal</b><span class="muted">Money, health, tasks and habits in one place</span></button>
    <button class="tile mt-notes-tile" onclick="MT_openPage('notes')"><div class="tile-icon">📝</div><b>Notes</b><span class="muted">Write notes and sync with Google Sheet</span></button>
    <button class="tile" onclick="MT_openPage('settings')"><div class="tile-icon">⚙️</div><b>Settings</b><span class="muted">Tracker settings and configuration</span></button>
  </div>
</div>
</section>

<section id="money" class="page">
<div class="inner money-dashboard-shell">
<h1>💰 Money</h1>
<p class="muted">Your uploaded and manually entered money data.</p>

<!-- V109: Quick Manual Entry is always at the top -->
<div class="card money-quick-entry-card" id="moneyQuickEntryCard">
  <div class="money-quick-entry-head">
    <div>
      <h2>✍️ Manual Data Entry</h2>
      <p class="muted">Enter a transaction quickly. Categories are loaded directly from the Google Sheet <b>help</b> tab.</p>
    </div>
    <div class="money-quick-entry-actions">
      <span id="moneyQuickCategoryStatus" class="muted">Categories not refreshed yet</span>
      <button class="secondary" onclick="refreshMoneyCategories(true)">↻ Refresh Categories</button>
    </div>
  </div>
  <div id="moneyQuickEntry"></div>
</div>

<!-- Keep the familiar Money screen first -->
<div class="card google-sync-panel">
  <div class="google-sync-row">
    <div>
      <b>🔗 Google Sheet Connection</b> <span style="font-size:10px;color:#64748b">V54 DATE-SAFE</span>
      <div id="googleSyncStatus" class="muted">Not connected yet</div>
    </div>
    <div class="google-sync-actions">
      <button class="primary" onclick="connectGoogleSheet()">Connect & Load</button>
      <button class="secondary" onclick="MW_manualMasterSync()">Sync Now</button>
    </div>
  </div>
  <div class="note" style="margin-top:10px">
    This version is hosted inside Google Apps Script, so no cross-origin network permission is required. Click <b>Connect & Load</b>.
  </div>
</div>

<div class="grid money-original-grid">
  <button class="tile money-income-card" onclick="openMoneyCategoryTransactions('Income')">
    <div class="tile-icon">💵</div><b>Income</b>
    <div id="moneyIncome" class="count" style="font-size:30px">₹0.00</div>
    <span id="moneyIncomeCount" class="muted">0 transactions</span>
  </button>

  <button class="tile money-expense-card" onclick="openMoneyCategoryTransactions('Expenses')">
    <div class="tile-icon">💸</div><b>Expenses</b>
    <div id="moneyExpenses" class="count" style="font-size:30px">₹0.00</div>
    <span id="moneyExpenseCount" class="muted">0 transactions</span>
  </button>

  <button class="tile money-savings-card" onclick="openMoneyCategoryTransactions('Savings')">
    <div class="tile-icon">🏦</div><b>Savings</b>
    <div id="moneySavings" class="count" style="font-size:30px">₹0.00</div>
    <span id="moneySavingsCount" class="muted">0 transactions</span>
  </button>

  <button class="tile money-loan-took-card" onclick="openMoneyCategoryTransactions('Loan I Took')">
    <div class="tile-icon">📥</div><b>Loan I Took</b>
    <div id="moneyLoanTook" class="count" style="font-size:30px">₹0.00</div>
    <span id="moneyLoanTookCount" class="muted">0 transactions</span>
  </button>

  <button class="tile money-loan-gave-card" onclick="openMoneyCategoryTransactions('Loan I Gave')">
    <div class="tile-icon">📤</div><b>Loan I Gave</b>
    <div id="moneyLoanGave" class="count" style="font-size:30px">₹0.00</div>
    <span id="moneyLoanGaveCount" class="muted">0 transactions</span>
  </button>

  <button class="tile money-remaining-card money-remaining-clickable" onclick="openAccountBalancePopup()">
    <div class="tile-icon">💰</div><b>Remaining Amount</b>
    <div id="moneyRemaining" class="count" style="font-size:30px">₹0.00</div>
    <span class="muted">Click to view balance by account</span>
  </button>

  <button class="tile money-forecast-card" onclick="openMoneyForecast()">
    <div class="tile-icon">🔮</div><b>Forecast</b>
    <span class="muted">Monthly free cash, safe-to-spend and next month outlook</span>
  </button>

  <button class="tile money-others-card" onclick="openMoneyOthers()">
    <div class="tile-icon">🧰</div><b>Others</b>
    <span class="muted">Upload, sheet data, view options and clear data</span>
  </button>
</div>

<!-- New visual insights come AFTER the familiar cards -->
<div class="money-insights-heading">
  <div><div class="money-eyebrow">VISUAL INSIGHTS</div><h2>Graphs & Recent Activity</h2><p class="muted">Category comparison first, followed by breakdowns, trends, movement and recent transactions.</p></div>
</div>

<div class="money-chart-card">
  <div class="money-card-title-row"><div><h3>All Category Comparison</h3><p>Compare totals and immediately see where your money is highest and lowest.</p></div></div>
  <div id="moneyAllCategoryChart" class="money-all-category-chart"></div><div id="moneyHighLowSummary" class="money-high-low-summary"></div>
</div>

<div class="money-chart-card money-breakdown-card">
  <div class="money-card-title-row"><div><h3>Expense Breakdown</h3><p>Where your spending goes</p></div></div>
  <div class="money-donut-layout"><div id="moneyExpenseDonut" class="money-donut"><div class="money-donut-center"><small>Total Expense</small><b id="moneyDonutTotal">₹0.00</b></div></div><div id="moneyExpenseLegend" class="money-breakdown-list"></div></div>
</div>

<div class="money-chart-card">
  <div class="money-card-title-row"><div><h3>Savings Snapshot</h3><p>How your savings are distributed</p></div></div><div id="moneySavingsBars" class="money-progress-list"></div>
</div>

<div class="money-chart-card money-subcategory-overview-card">
  <div class="money-card-title-row"><div><h3>Sub Category Overview <span class="money-overall-badge">Overall Transactions</span></h3><p>All sub categories from every main category · based on overall transactions (all time).</p></div></div>
  <div class="money-sub-info-note">This shows where your money comes from or goes in total across all time. Transfer In / Transfer Out are excluded.</div>
  <div class="money-filter-title">Main Category — include / exclude from graph</div><div id="moneySubCategoryFilterChecks" class="money-category-checks"></div>
  <div class="money-sub-table-head"><span>Sub Category</span><span>Amount</span><span>% of Total</span></div><div id="moneySubCategoryOverallBars" class="money-overall-sub-bars"></div><div id="moneySubCategoryTotalsCards" class="money-sub-summary-cards"></div><div id="moneySubCategoryGrandTotal" class="money-sub-grand-total"></div>
</div>

<div class="money-chart-card money-cashflow-card">
  <div class="money-card-title-row"><div><h3>Cash Flow Trend</h3><p>Income vs expenses vs savings — recent 6 months</p></div><div class="money-legend"><span><i class="legend-income"></i>Income</span><span><i class="legend-expense"></i>Expenses</span><span><i style="background:#2563eb"></i>Savings</span></div></div><div id="moneyCashFlowChart" class="money-svg-chart"></div>
</div>

<div class="money-chart-card">
  <div class="money-card-title-row"><div><h3>Monthly Category Trend</h3><p>Select a category to see its monthly highs and lows.</p></div></div><div id="moneyCategoryTrendTabs" class="money-trend-tabs"></div><div id="moneySelectedCategorySummary" class="money-selected-category-summary"></div><div id="moneySelectedCategoryChart" class="money-svg-chart"></div>
</div>

<div class="money-chart-card">
  <div class="money-card-title-row"><div><h3>Money Movement</h3><p>Transfers and loans shown separately</p></div></div><div class="money-movement-grid"><div class="movement-stat"><span>Transfer In</span><b id="moneyTransferIn">₹0.00</b><small>Internal movement</small></div><div class="movement-stat"><span>Transfer Out</span><b id="moneyTransferOut">₹0.00</b><small>Internal movement</small></div><button class="movement-stat" onclick="openMoneyCategoryTransactions('Loan I Took')"><span>Loan In</span><b id="moneyLoanInVisual">₹0.00</b><small>Cash received as loan</small></button><button class="movement-stat" onclick="openMoneyCategoryTransactions('Loan I Gave')"><span>Loan Out</span><b id="moneyLoanOutVisual">₹0.00</b><small>Cash given / repaid</small></button></div>
</div>

<div class="money-chart-card money-recent-card"><div class="money-card-title-row"><div><h3>Recent Transactions</h3><p>Your latest money activity</p></div><button class="secondary" onclick="openMoneyOthers();setTimeout(function(){closeMoneyOthers();openViewOptions()},50)">View Options</button></div><div id="moneyRecentVisual"></div></div>

<div id="moneyModule" class="card money-module"></div>
</div>
</section>





<section id="stocks" class="page">
<div class="inner stock-hub-shell">

  <div class="stock-hub-head">
    <div>
      <h1>📈 Stocks</h1>
      <p class="muted">Choose what you want to see. The scanner loads only when you open it.</p>
    </div>
  </div>

  <div class="stock-tool-icons">
    <button class="stock-tool-card" id="stOldViewIcon" onclick="ST_showTool('previous',this)">
      <span class="stock-tool-emoji">📋</span>
      <b>Previous Stocks</b>
      <small>Your earlier Stocks section</small>
    </button>

    <button class="stock-tool-card" id="stScannerIcon" onclick="ST_showTool('scanner',this)">
      <span class="stock-tool-emoji">📊</span>
      <b>₹100 Scanner</b>
      <small>1D / 1W / 6M / 1Y / Custom</small>
    </button>

    <button class="stock-tool-card stock-tool-pro" id="stProIcon" onclick="ST_showTool('pro',this)">
      <span class="stock-tool-emoji">🧠</span>
      <b>Pro Stock Analyzer</b>
      <small>Trend · RSI · EMA · Bollinger · 52W · Signals</small>
    </button>

    <button class="stock-tool-card stock-tool-nsepro" id="stNseProIcon" onclick="window.open('https://nse-pro-stock-analyzer-fhpztdw6j5rvb5dxkyvdt8.streamlit.app','_blank','noopener,noreferrer')">
      <span class="stock-tool-emoji">🚀</span>
      <b>NSE PRO</b>
      <small>Live Analyzer · Swing Screeners · All NSE Performance · News · Brokerage Calls</small>
    </button>
  </div>

  <div id="stPreviousTool" class="stock-tool-panel">
    <div class="stock-tool-panel-head">
      <div>
        <h2>📋 Previous Stocks</h2>
        <p class="muted">Previous section kept separately as requested.</p>
      </div>
      <button class="secondary" onclick="ST_closeTools()">✕ Close</button>
    </div>

    <div class="card stock-previous-placeholder">
      <h3>Previous Stocks View</h3>
      <p class="muted">Your earlier Stocks section is kept as its own icon. The new ₹100 scanner does not replace this section.</p>
      <div class="stock-prev-note">
        Use <b>₹100 Scanner</b> for performance ranking. This icon is reserved for the previous Stocks dashboard/tools you were already using.
      </div>
    </div>
  </div>

  <div id="stScannerTool" class="stock-tool-panel">
    <div class="stock-tool-panel-head">
      <div>
        <h2>📊 Stock Performance Scanner</h2>
        <p class="muted">Compare every stock using the same ₹100 starting value.</p>
      </div>
      <button class="secondary" onclick="ST_closeTools()">✕ Close</button>
    </div>

    <div class="card st-sync-card">
      <div>
        <b>Google Sheet: stocks</b>
        <div id="stSyncStatus" class="muted">Open the scanner to load data.</div>
      </div>
      <div class="st-sync-actions">
        <div id="stDateRange" class="st-date-range">—</div>
        <button class="secondary" onclick="ST_sync(true,true)">↻ Refresh Data</button>
      </div>
    </div>

    <div class="card st-controls">
      <div class="st-period-buttons">
        <button class="active" data-st-period="1D" onclick="ST_setPeriod('1D',this)">1 Day</button>
        <button data-st-period="1W" onclick="ST_setPeriod('1W',this)">1 Week</button>
        <button data-st-period="6M" onclick="ST_setPeriod('6M',this)">6 Months</button>
        <button data-st-period="1Y" onclick="ST_setPeriod('1Y',this)">1 Year</button>
        <button data-st-period="CUSTOM" onclick="ST_setPeriod('CUSTOM',this)">Custom</button>
      </div>

      <div id="stCustomControls" class="st-custom-controls">
        <span>Custom trading days:</span>
        <button data-st-custom="2" onclick="ST_setCustomDays(2,this)">2</button>
        <button data-st-custom="3" onclick="ST_setCustomDays(3,this)">3</button>
        <button class="active" data-st-custom="4" onclick="ST_setCustomDays(4,this)">4</button>
        <button data-st-custom="8" onclick="ST_setCustomDays(8,this)">8</button>
      </div>

      <div class="st-search-row st-search-row-v108">
<input id="stSearch" placeholder="Search symbol, ticker or company..." oninput="ST_render()">
<select id="stSectorFilter" onchange="ST_render()"><option value="ALL">All Sectors</option></select>
<select id="stCapFilter" onchange="ST_render()"><option value="ALL">All Market Caps</option></select>
<select id="stMinHistory" onchange="ST_render()"><option value="0">Show all stocks</option><option value="1">Full selected history only</option></select>
</div>
    </div>

    <div class="st-summary-grid">
      <div class="card st-summary">
        <span>Period</span>
        <b id="stSummaryPeriod">1 Day</b>
        <small id="stSummaryDates">—</small>
      </div>
      <div class="card st-summary">
        <span>Stocks Compared</span>
        <b id="stSummaryCount">0</b>
        <small>Valid start + latest price</small>
      </div>
      <div class="card st-summary st-best">
        <span>Best ₹100 Value</span>
        <b id="stSummaryBest">—</b>
        <small id="stSummaryBestStock">—</small>
      </div>
      <div class="card st-summary st-worst">
        <span>Lowest ₹100 Value</span>
        <b id="stSummaryWorst">—</b>
        <small id="stSummaryWorstStock">—</small>
      </div>
    </div>

    <div class="card st-period-date-strip"><div><span>Selected Period</span><b id="stPeriodTitle">1 Day Performance</b></div><div><span>Start Date</span><b id="stGlobalStartDate">—</b></div><div><span>Latest Date</span><b id="stGlobalLatestDate">—</b></div></div>
<div class="card st-table-card">
      <div class="st-table-head">
        <div>
          <h2>₹100 Performance Ranking</h2>
          <p class="muted">₹100 Value = (Latest Price ÷ Start Price) × 100. Highest value is ranked first.</p>
        </div>
        <div class="st-table-actions">
          <button class="secondary" onclick="ST_toggleOnlyGainers()">Gainers Only</button>
          <button class="secondary" onclick="ST_toggleOnlyLosers()">Losers Only</button>
          <button class="secondary" onclick="ST_resetFilters()">All</button>
        </div>
      </div>

      <div class="st-table-wrap">
        <table class="st-table">
          <thead>
            <tr><th>Rank</th><th>Stock</th><th>Company</th><th>Sector</th><th>Cap</th><th>Start ₹</th><th>Latest ₹</th><th>Avg ₹</th><th>Return %</th><th>₹100 Value</th><th>Trend</th></tr>
          </thead>
          <tbody id="stTableBody">
            <tr><td colspan="11" class="st-empty">Click ₹100 Scanner to load stocks.</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>


  <div id="stProTool" class="stock-tool-panel stp-v111-shell">
    <div class="stp-v111-topbar">
      <div>
        <div class="stp-v111-kicker">INTERNET MARKET DATA · NSE ANALYZER</div>
        <h2>🧠 Pro Stock Analyzer</h2>
        <p>Independent from your Google Sheet. Enter an NSE symbol and analyze live/latest market history from the internet.</p>
      </div>
      <div class="stp-v111-top-actions">
        <span id="stpProviderStatus" class="stp-v111-provider">● Internet engine ready</span>
        <button onclick="STP_analyzeCurrent(true)">↻ Refresh Market</button>
        <button onclick="ST_closeTools()">✕ Close</button>
      </div>
    </div>

    <div class="stp-v111-layout">
      <aside class="stp-v111-sidebar">
        <section>
          <h3>🔎 Search & Select Stock</h3>
          <label>NSE ticker or company</label>
          <div class="stp-v111-searchbox">
            <input id="stpSearch" placeholder="TBZ, ITC, TCS, SUZLON..." autocomplete="off"
                   oninput="STP_scheduleSearch()" onkeydown="if(event.key==='Enter')STP_analyzeCurrent(false)">
            <button onclick="STP_analyzeCurrent(false)">Analyze</button>
          </div>
          <div id="stpMatches" class="stp-v111-matches"></div>
        </section>

        <section>
          <h3>🗓️ Timeframe & Interval</h3>
          <label>Period</label>
          <select id="stpWindow" onchange="STP_renderInternetAnalysis()">
            <option value="22">1 Month</option>
            <option value="66">3 Months</option>
            <option value="132">6 Months</option>
            <option value="252" selected>1 Year</option>
          </select>
          <label>Candle interval</label>
          <select disabled>
            <option>Daily (1D)</option>
          </select>
        </section>

        <section>
          <h3>📐 Chart Overlays</h3>
          <label class="stp-v111-check"><input type="checkbox" id="stpSma20" checked onchange="STP_drawInternetChart()"> SMA 20</label>
          <label class="stp-v111-check"><input type="checkbox" id="stpSma50" checked onchange="STP_drawInternetChart()"> SMA 50</label>
          <label class="stp-v111-check"><input type="checkbox" id="stpSma200" onchange="STP_drawInternetChart()"> SMA 200</label>
          <label class="stp-v111-check"><input type="checkbox" id="stpEma9" checked onchange="STP_drawInternetChart()"> EMA 9</label>
          <label class="stp-v111-check"><input type="checkbox" id="stpBb" checked onchange="STP_drawInternetChart()"> Bollinger Bands</label>
          <label class="stp-v111-check"><input type="checkbox" id="stpSupport" checked onchange="STP_drawInternetChart()"> Support / Resistance</label>
        </section>

        <section>
          <h3>⚙️ Analysis Modules</h3>
          <div class="stp-v111-mini-feature">📊 Trend & Moving Averages</div>
          <div class="stp-v111-mini-feature">⚡ Momentum & RSI / MACD</div>
          <div class="stp-v111-mini-feature">🛡️ ATR Risk Management</div>
          <div class="stp-v111-mini-feature">🎯 Support / Resistance</div>
          <div class="stp-v111-mini-feature">📦 Volume Confirmation</div>
        </section>

        <div class="stp-v111-note">
          Data source is separate from your Sheet-based ₹100 Scanner. Market data may be delayed depending on the provider/exchange.
        </div>
      </aside>

      <main class="stp-v111-main">
        <div id="stpLoading" class="stp-v111-loader" style="display:none">
          <div class="stp-v111-spinner"></div>
          <b>Analyzing market data…</b>
          <span>Downloading history and calculating technical indicators.</span>
        </div>

        <div id="stpEmpty" class="stp-v111-hero-empty">
          <div>📈</div>
          <h1>Internet Pro Stock Analyzer</h1>
          <p>Search any NSE ticker to generate a technical dashboard with trend, momentum, swing setup and risk levels.</p>
          <div class="stp-v111-popular">
            <button onclick="STP_quickAnalyze('TBZ')">TBZ</button>
            <button onclick="STP_quickAnalyze('ITC')">ITC</button>
            <button onclick="STP_quickAnalyze('TCS')">TCS</button>
            <button onclick="STP_quickAnalyze('RELIANCE')">RELIANCE</button>
            <button onclick="STP_quickAnalyze('SUZLON')">SUZLON</button>
          </div>
        </div>

        <div id="stpContent" style="display:none">
          <div class="stp-v111-stock-header">
            <div>
              <div class="stp-v111-symbol-row">
                <h1 id="stpSymbol">—</h1>
                <span id="stpExchange" class="stp-v111-chip">NSE</span>
                <span id="stpMarketState" class="stp-v111-chip stp-v111-live">INTERNET</span>
              </div>
              <div id="stpCompany" class="stp-v111-subtitle">Internet market-data analysis</div>
            </div>
            <div class="stp-v111-lastupdate">
              <span>Latest session</span>
              <b id="stpLatestDate">—</b>
            </div>
          </div>

          <div class="stp-v111-kpis">
            <div class="stp-v111-kpi">
              <span>Current / Latest Price</span>
              <b id="stpPrice">—</b>
              <small id="stpDayChange">—</small>
            </div>
            <div class="stp-v111-kpi">
              <span>52-Week Range</span>
              <b id="stpRange">—</b>
              <small id="stpNearHigh">—</small>
            </div>
            <div class="stp-v111-kpi">
              <span>RSI (14)</span>
              <b id="stpRsi">—</b>
              <small id="stpRsiText">—</small>
            </div>
            <div class="stp-v111-kpi">
              <span>Technical Consensus</span>
              <b id="stpConsensus">—</b>
              <small id="stpScore">—</small>
            </div>
            <div class="stp-v111-kpi">
              <span>20D Momentum</span>
              <b id="stpMom20">—</b>
              <small id="stpMomText">—</small>
            </div>
          </div>

          <div class="stp-v111-chart-card">
            <div class="stp-v111-chart-head">
              <div>
                <h2>📈 Price Action & Technical Overlays</h2>
                <p id="stpChartSub">Daily OHLC history from the internet market-data engine.</p>
              </div>
              <div class="stp-v111-legend">
                <span><i class="price"></i>Price</span>
                <span><i class="sma20"></i>SMA20</span>
                <span><i class="sma50"></i>SMA50</span>
                <span><i class="ema9"></i>EMA9</span>
              </div>
            </div>
            <svg id="stpChart" viewBox="0 0 1280 470" preserveAspectRatio="none"></svg>
          </div>

          <div class="stp-v111-signal-grid">
            <section class="stp-v111-signal-card">
              <div class="stp-v111-signal-heading">
                <h2>🎯 Medium-Term Investment</h2>
                <span>1–6 Months</span>
              </div>
              <div id="stpMediumBadge" class="stp-v111-rec">—</div>
              <p id="stpMediumText"></p>
              <h3>Key Investment Factors</h3>
              <div id="stpMediumFactors" class="stp-v111-factors"></div>
            </section>

            <section class="stp-v111-signal-card">
              <div class="stp-v111-signal-heading">
                <h2>⚡ Short-Term Swing Trade</h2>
                <span>Days–2 Weeks</span>
              </div>
              <div id="stpSwingBadge" class="stp-v111-rec">—</div>
              <p id="stpSwingText"></p>
              <h3>Active Trade Setups</h3>
              <div id="stpSwingFactors" class="stp-v111-factors"></div>
            </section>
          </div>

          <section class="stp-v111-risk-card">
            <div class="stp-v111-section-title">
              <h2>🛡️ Trade Execution & Risk Management Levels</h2>
              <span>ATR + support/resistance based technical framework</span>
            </div>
            <div class="stp-v111-risk-grid">
              <div><span>Reference Entry</span><b id="stpEntry">—</b><small>Latest market price</small></div>
              <div><span>Stop Loss</span><b id="stpSL">—</b><small id="stpSLPct">—</small></div>
              <div><span>Target 1</span><b id="stpT1">—</b><small id="stpT1Pct">—</small></div>
              <div><span>Target 2</span><b id="stpT2">—</b><small id="stpT2Pct">—</small></div>
              <div><span>Risk : Reward</span><b id="stpRR">—</b><small>Using Target 2</small></div>
            </div>
          </section>

          <section class="stp-v111-tech-card">
            <div class="stp-v111-section-title">
              <h2>🧪 Technical Indicator Dashboard</h2>
              <span>Calculated from downloaded OHLCV history</span>
            </div>
            <div class="stp-v111-indicator-grid">
              <div><span>SMA 20</span><b id="stpSma20v">—</b><small id="stpSma20s">—</small></div>
              <div><span>SMA 50</span><b id="stpSma50v">—</b><small id="stpSma50s">—</small></div>
              <div><span>SMA 200</span><b id="stpSma200v">—</b><small id="stpSma200s">—</small></div>
              <div><span>EMA 9 / 20</span><b id="stpEmaPair">—</b><small id="stpEmaSignal">—</small></div>
              <div><span>MACD</span><b id="stpMacd">—</b><small id="stpMacdSignal">—</small></div>
              <div><span>ADX (14)</span><b id="stpAdx">—</b><small id="stpAdxText">—</small></div>
              <div><span>ATR (14)</span><b id="stpAtr">—</b><small id="stpAtrText">—</small></div>
              <div><span>Supertrend</span><b id="stpSupertrend">—</b><small id="stpSupertrendText">—</small></div>
              <div><span>Bollinger Position</span><b id="stpBoll">—</b><small id="stpBollText">—</small></div>
              <div><span>20D Up Days</span><b id="stpUpDays">—</b><small id="stpUpText">—</small></div>
              <div><span>Support</span><b id="stpSupportV">—</b><small>Recent technical floor</small></div>
              <div><span>Resistance</span><b id="stpResistanceV">—</b><small>Recent technical ceiling</small></div>
            </div>
          </section>

          <div class="stp-v111-disclaimer">
            Technical signals are rule-based decision support, not guaranteed predictions or personalized investment advice.
          </div>
        </div>
      </main>
    </div>
  </div>

</div>
</section>


<section id="time" class="page">
<div class="inner time-planner-shell">

  <div class="time-page-head">
    <div>
      <h1>⏱️ Smart Daily Planner</h1>
      <p class="muted">Plan → Prioritize → Auto-schedule → Focus → Complete.</p>
    </div>
    <div class="tb-date-actions">
      <button class="secondary" onclick="TB_changePlanDate(-1)">←</button>
      <input id="tbPlanDate" type="date" onchange="TB_setPlanDate(this.value)">
      <button class="secondary" onclick="TB_changePlanDate(1)">→</button>
      <button class="secondary" onclick="TB_goToday()">Today</button>
    </div>
  </div>

  
<div id="tbTodayBrief" class="tb-today-brief"></div>

<div class="card tb-status-dashboard">
  <div class="tb-status-top-head">
    <div>
      <h2 id="tbStatusPeriodTitle">📌 Task Status — Today</h2>
      <p id="tbStatusPeriodSubtitle" class="muted">See your workload immediately before planning the day.</p>
    </div>
    <div id="tbStatusTotalToday" class="tb-status-total">0 tasks</div>
  </div>
  <div class="tb-status-period-row">
    <button class="active" onclick="TB_setStatusPeriod('Today',this)">Today</button>
    <button onclick="TB_setStatusPeriod('Week',this)">This Week</button>
    <button onclick="TB_setStatusPeriod('Month',this)">This Month</button>
    <button onclick="TB_setStatusPeriod('Year',this)">This Year</button>
    <button onclick="TB_setStatusPeriod('Overall',this)">Overall</button>
  </div>

  <div class="tb-status-summary-grid">
    <button type="button" class="tb-status-summary-card not-started" data-task-status="Not Started" onclick="TB_openStatusDetails('Not Started')">
      <span>Not Started</span>
      <b id="tbStatusNotStarted">0</b>
      <small>Waiting to begin</small>
    </button>
    <button type="button" class="tb-status-summary-card in-progress" data-task-status="In Progress" onclick="TB_openStatusDetails('In Progress')">
      <span>In Progress</span>
      <b id="tbStatusInProgress">0</b>
      <small>Currently active</small>
    </button>
    <button type="button" class="tb-status-summary-card done" data-task-status="Done" onclick="TB_openStatusDetails('Done')">
      <span>Done</span>
      <b id="tbStatusDone">0</b>
      <small>Completed today</small>
    </button>
    <button type="button" class="tb-status-summary-card hold" data-task-status="Hold" onclick="TB_openStatusDetails('Hold')">
      <span>Hold</span>
      <b id="tbStatusHold">0</b>
      <small>Waiting for your decision</small>
    </button>
  </div>
</div>

<div class="tb-command-center">
  <button class="tb-command-btn" onclick="TB_showTimeTool('tbQuickPanel',this)"><span>⏱️</span><b>Time & Focus</b><small>Clock and timer</small></button>
  <button class="tb-command-btn" onclick="TB_showTimeTool('tbBrainPanel',this)"><span>🧠</span><b>Brain Dump</b><small>Quick task capture</small></button>
  <button class="tb-command-btn" onclick="TB_showTimeTool('tbRecurringPanel',this)"><span>🔁</span><b>Recurring</b><small>Routine and bills</small></button>
  <button class="tb-command-btn primary-command" onclick="TB_showTimeTool('tbSmartPlanPanel',this)"><span>📅</span><b>Smart Time</b><small>Edit today's plan</small></button>
  <button class="tb-command-btn" onclick="TB_showTimeTool('tbAnalyticsPanel',this)"><span>📊</span><b>Analytics</b><small>Progress history</small></button>
</div>

  <div id="tbQuickPanel" class="tb-top-grid tb-tool-panel">
<div class="tb-panel-close-row tb-panel-close-row-grid"><b>⏱️ Time & Focus</b><button onclick="TB_closeTimeTool('tbQuickPanel')">✕ Close</button></div>
    <div class="card tb-remaining-card">
      <div class="tb-small-label">CURRENT TIME</div>
      <div id="tbCurrentClock" class="tb-big-number">--:--:--</div>
      <div class="tb-mini-row">
        <span>Remaining today</span>
        <b id="tbDayRemaining">00h 00m</b>
      </div>
    </div>

    <div class="card tb-focus-card">
      <div class="tb-focus-head">
        <div>
          <div class="tb-small-label">FOCUS TIMER</div>
          <div id="tbTimerDisplay" class="tb-timer-display">20:00</div>
        </div>
        <select id="tbTimerTask" class="tb-task-select"></select>
      </div>

      <div class="tb-timer-presets">
        <button onclick="TB_setTimer(2)">2m</button>
        <button onclick="TB_setTimer(20)">20m</button>
        <button onclick="TB_setTimer(25)">25m</button>
        <button onclick="TB_setTimer(45)">45m</button>
        <button onclick="TB_setTimer(60)">60m</button>
        <label class="tb-custom-minutes">
          <input id="tbCustomMinutes" type="number" min="1" max="480" placeholder="Min">
          <button onclick="TB_setCustomTimer()">Set</button>
        </label>
      </div>

      <div class="tb-timer-actions">
        <button class="primary" onclick="TB_startTimer()">▶ Start</button>
        <button class="secondary" onclick="TB_pauseTimer()">Ⅱ Pause</button>
        <button class="secondary" onclick="TB_resetTimer()">↺ Reset</button>
        <button class="secondary" onclick="TB_addFiveMinutes()">+5m</button>
      </div>
    </div>

    <div class="card tb-month-card">
      <div class="tb-small-label">THIS MONTH</div>
      <div class="tb-month-stats">
        <div><b id="tbMonthDone">0</b><span>Done</span></div>
        <div><b id="tbMonthFocus">0m</b><span>Focused</span></div>
        <div><b id="tbMonthHold">0</b><span>Hold</span></div>
        <div><b id="tbMonthMoved">0</b><span>Moved</span></div>
      </div>
    </div>
  </div>

  <div class="tb-work-grid">
    <div id="tbBrainPanel" class="card tb-priority-panel tb-tool-panel">
<div class="tb-panel-close-row"><b>🧠 Brain Dump</b><button onclick="TB_closeTimeTool('tbBrainPanel')">✕ Close</button></div>
      

<div class="tb-section-head">
  <div>
    <h2>🧠 Brain Dump</h2>
    <p class="muted">Every comma creates a new task — repeated task names are allowed. Refresh clears only this writing area; already-created tasks stay in your task list.</p>
  </div>
  <button type="button" class="tb-brain-refresh-btn" onclick="TB_refreshBrainDump()">↻ Refresh Brain Dump</button>
</div>

<div class="tb-brain-paper">
  <textarea id="tbBrainInput"
    placeholder="Example: Finish CAD report, Buy vegetables, Call bank, Learn Python..."
    oninput="TB_brainInputChanged(this)"></textarea>
  <div class="tb-brain-hint">Tip: each comma creates one task. Example: <b>Delivery, Delivery, Delivery,</b> creates 3 separate tasks.</div>
</div>




      
<div class="tb-divider"></div>

    </div>

    <div id="tbSmartPlanPanel" class="card tb-day-plan-panel tb-tool-panel" style="margin-top:0">
<div class="tb-panel-close-row"><b>📅 Smart Time</b><button onclick="TB_closeTimeTool('tbSmartPlanPanel')">✕ Close</button></div>
      <div class="tb-section-head">
        <div>
          <h2>📅 Smart Day Plan</h2>
          <p id="tbPlanDateLabel" class="muted">Tasks assigned to this date are shown here automatically. Edit start time, minutes or status directly.</p><div class="tb-live-plan-legend"><span><i class="fixed"></i>Manual time</span><span><i class="priority"></i>Auto planned</span><span><i class="routine"></i>Recurring</span></div>
        </div>
        <div class="tb-plan-actions">
          <button class="secondary" onclick="TB_rebuildSmartTime()">↻ Rebuild Plan</button>
          <button class="secondary" onclick="TB_scrollToNow()">⏱ Current Time</button>
        </div>
      </div>
      <div class="tb-sleep-strip">
        <span>🌙 Sleep window hidden</span>
        <b>23:00 – 06:00</b>
        <small>7 hours</small>
      </div>
      <div id="tb24HourGrid" class="tb-smart-day-windows"></div>
    </div>
  </div>

  



<div id="tbRecurringPanel" class="tb-recurring-card tb-tool-panel">
  <div class="tb-panel-close-row">
    <b>🔁 Recurring & Mandatory</b>
    <button onclick="TB_closeTimeTool('tbRecurringPanel')">✕ Close</button>
  </div>

  <div class="tb-section-head">
    <div>
      <h2>🔁 Recurring Tasks</h2>
      <p class="muted">Create routines once. On each matching day they automatically become normal daily tasks and are included in Not Started / In Progress / Done / Hold counts.</p>
    </div>
    <button class="primary" onclick="TB_addRecurring()">＋ Add Recurring Rule</button>
  </div>

  <div class="tb-recurring-summary">
    <button onclick="TB_openRecurringDetails('All')">
      <span>Scheduled Today</span><b id="tbRecurringScheduledCount">0</b><small>generated daily tasks</small>
    </button>
    <button class="done" onclick="TB_openRecurringDetails('Done')">
      <span>Done</span><b id="tbRecurringDoneCount">0</b><small>completed today</small>
    </button>
    <button class="pending" onclick="TB_openRecurringDetails('Not Done')">
      <span>Pending</span><b id="tbRecurringPendingCount">0</b><small>still active</small>
    </button>
  </div>

  <div class="tb-recurring-filter-row">
    <button class="active" onclick="TB_setRecurringFilter('All',this)">All</button>
    <button onclick="TB_setRecurringFilter('Daily',this)">Daily</button>
    <button onclick="TB_setRecurringFilter('Weekdays',this)">Mon–Fri</button>
    <button onclick="TB_setRecurringFilter('Weekends',this)">Sat–Sun</button>
    <button onclick="TB_setRecurringFilter('Weekly',this)">Weekly</button>
    <button onclick="TB_setRecurringFilter('Monthly',this)">Monthly</button>
    <button onclick="TB_setRecurringFilter('Yearly',this)">Yearly</button>
  </div>

  <div class="tb-recurring-brain card">
    <div class="tb-section-head">
      <div>
        <h3>🧠 Recurring Brain Dump</h3>
        <p class="muted">Choose the repeat rule, then type tasks separated by commas. Every comma creates one recurring rule.</p>
      </div>
      <button type="button" class="tb-brain-refresh-btn" onclick="TB_refreshRecurringBrainDump()">↻ Refresh</button>
    </div>

    <div class="tb-recurring-brain-controls">
      <label>Repeat
        <select id="tbRecurringBrainKind" onchange="TB_recurringBrainConfigChanged()">
          <option>Daily</option>
          <option>Weekdays</option>
          <option>Weekends</option>
          <option>Weekly</option>
          <option>Monthly</option>
          <option>Yearly</option>
        </select>
      </label>
      <label id="tbRecurringBrainDayWrap">Day / Date
        <span id="tbRecurringBrainDayField"></span>
      </label>
      <label>Start
        <input id="tbRecurringBrainStart" type="time" value="08:00" onchange="TB_recurringBrainConfigChanged(false)">
      </label>
      <label>Minutes
        <input id="tbRecurringBrainMinutes" type="number" min="1" value="20" onchange="TB_recurringBrainConfigChanged(false)">
      </label>
      <label>Type
        <select id="tbRecurringBrainType" onchange="TB_recurringBrainConfigChanged(false)">
          <option>Personal</option><option>Job</option><option>Money</option>
          <option>Health</option><option>Learning</option><option>Other</option>
        </select>
      </label>
    </div>

    <textarea id="tbRecurringBrainInput"
      class="tb-recurring-brain-input"
      placeholder="Example: Walking, Gym, Pay Rent,"
      oninput="TB_recurringBrainInputChanged(this)"></textarea>
    <div class="tb-brain-hint">Examples: <b>Daily</b> → Walking, Gym · <b>Weekdays</b> → Office · <b>Weekends</b> → House cleaning · <b>Monthly</b> day 2 → Rent · <b>Yearly</b> → Birthday reminder.</div>
  </div>

  <div class="tb-recurring-head tb-recurring-head-v96">
    <span>Task</span>
    <span>Repeat</span>
    <span>Day / Date</span>
    <span>Start</span>
    <span>Min</span>
    <span>Type</span>
    <span>Active</span>
    <span></span>
  </div>

  <div id="tbRecurringRows" class="tb-recurring-list"></div>
</div>

<div id="tbAnalyticsPanel" class="card tb-status-analytics-panel tb-tool-panel">
<div class="tb-panel-close-row"><b>📊 Analytics</b><button onclick="TB_closeTimeTool('tbAnalyticsPanel')">✕ Close</button></div>
  <div class="tb-section-head">
    <div>
      <h2>📊 Task Status Analytics</h2>
      <p class="muted">Review task movement across different periods.</p>
    </div>
    <div class="tb-analytics-tabs">
      <button class="active" onclick="TB_setAnalyticsPeriod('Overall',this)">Overall</button>
      <button onclick="TB_setAnalyticsPeriod('Daily',this)">Daily</button>
      <button onclick="TB_setAnalyticsPeriod('Weekly',this)">Weekly</button>
      <button onclick="TB_setAnalyticsPeriod('Monthly',this)">Monthly</button>
      <button onclick="TB_setAnalyticsPeriod('Yearly',this)">Yearly</button>
    </div>
  </div>

  <div id="tbAnalyticsSummary" class="tb-analytics-summary-grid"></div>
  <div id="tbAnalyticsChart" class="tb-analytics-chart"></div>
  <div id="tbAnalyticsDetails" class="tb-analytics-details"></div>
</div>

<div class="card tb-history-panel">
    <div class="tb-section-head"><div><h2>📊 Monthly Completion History</h2><p class="muted">Completed tasks this month with planned vs actual time.</p></div></div>
    <div id="tbMonthlyHistory"></div>
  </div>

</div>
</section>


<section id="health" class="page">
<div class="inner health-shell">

  <div class="health-head">
    <div>
      <h1>❤️ Health Tracker</h1>
      <p class="muted">Track what you eat, your weight and your sleep in one place.</p>
    </div>
    <div class="health-date-wrap">
      <button class="secondary" onclick="HL_changeDate(-1)">←</button>
      <input id="hlDate" type="date" onchange="HL_setDate(this.value)">
      <button class="secondary" onclick="HL_changeDate(1)">→</button>
      <button class="secondary" onclick="HL_goToday()">Today</button>
    </div>
  </div>

  <div class="health-summary-grid">
    <div class="health-summary-card health-cal-card">
      <span>Calories Today</span>
      <b id="hlCaloriesToday">0 kcal</b>
      <small id="hlMealCount">0 food entries</small>
    </div>
    <div class="health-summary-card health-weight-card">
      <span>Latest Weight</span>
      <b id="hlLatestWeight">— kg</b>
      <small id="hlWeightChange">No previous reading</small>
    </div>
    <div class="health-summary-card health-sleep-card">
      <span>Sleep</span>
      <b id="hlSleepToday">— h</b>
      <small id="hlSleepAverage">7-day average: —</small>
    </div>
  </div>

  <!-- FOOD -->
  <div class="card health-panel">
    <div class="health-section-head">
      <div>
        <h2>🍽️ Food & Calories</h2>
        <p class="muted">Choose a common food for automatic calories, or enter calories manually when needed.</p>
      </div>
      <button class="primary" onclick="HL_addFoodRow()">＋ Add Food</button>
    </div>

    <div class="health-meal-tabs" id="hlMealTabs">
      <button class="active" onclick="HL_setMealFilter('All',this)">All</button>
      <button onclick="HL_setMealFilter('Breakfast',this)">Breakfast</button>
      <button onclick="HL_setMealFilter('Lunch',this)">Lunch</button>
      <button onclick="HL_setMealFilter('Dinner',this)">Dinner</button>
      <button onclick="HL_setMealFilter('Snack',this)">Snack</button>
    </div>

    <div class="health-food-head">
      <span>Meal</span><span>Food</span><span>Qty</span><span>Unit</span><span>Calories</span><span></span>
    </div>
    <div id="hlFoodRows" class="health-food-rows"></div>

    <div class="health-calorie-total">
      <span>Total for selected day</span>
      <b id="hlFoodTotalBottom">0 kcal</b>
    </div>
  </div>

  <!-- WEIGHT + SLEEP -->
  <div class="health-two-col">
    <div class="card health-panel">
      <div class="health-section-head">
        <div>
          <h2>⚖️ Weight</h2>
          <p class="muted">Add one reading whenever you weigh yourself.</p>
        </div>
      </div>

      <div class="health-quick-form">
        <label>Date<input id="hlWeightDate" type="date"></label>
        <label>Weight (kg)<input id="hlWeightValue" type="number" step="0.1" min="1" placeholder="e.g. 72.5"></label>
        <button class="primary" onclick="HL_saveWeight()">Save Weight</button>
      </div>

      <div class="health-weight-stats">
        <div><span>Latest</span><b id="hlWeightLatest2">—</b></div>
        <div><span>7-day change</span><b id="hlWeight7Change">—</b></div>
        <div><span>30-day change</span><b id="hlWeight30Change">—</b></div>
      </div>

      <div id="hlWeightChart" class="health-weight-chart"></div>
      <div id="hlWeightHistory" class="health-small-table"></div>
    </div>

    <div class="card health-panel">
      <div class="health-section-head">
        <div>
          <h2>😴 Sleep</h2>
          <p class="muted">Enter sleep and wake time; duration is calculated automatically.</p>
        </div>
      </div>

      <div class="health-quick-form health-sleep-form">
        <label>Date<input id="hlSleepDate" type="date"></label>
        <label>Sleep time<input id="hlSleepStart" type="time" value="23:00"></label>
        <label>Wake time<input id="hlSleepEnd" type="time" value="06:00"></label>
        <button class="primary" onclick="HL_saveSleep()">Save Sleep</button>
      </div>

      <div class="health-sleep-preview">
        <span>Calculated sleep</span>
        <b id="hlSleepPreview">7h 00m</b>
      </div>

      <div class="health-weight-stats">
        <div><span>Last night</span><b id="hlSleepLast">—</b></div>
        <div><span>7-day avg</span><b id="hlSleep7Avg">—</b></div>
        <div><span>30-day avg</span><b id="hlSleep30Avg">—</b></div>
      </div>

      <div id="hlSleepChart" class="health-weight-chart"></div>
      <div id="hlSleepHistory" class="health-small-table"></div>
    </div>
  </div>

</div>
</section>


<section id="mind" class="page">
<div class="inner">
  <h1>🧠 Mind</h1>
  <div class="grid">
    <div class="tile"><div class="tile-icon">🧘</div><b>Meditation</b><span class="muted">Track meditation and quiet time</span></div>
    <div class="tile"><div class="tile-icon">😊</div><b>Mood</b><span class="muted">Track how you feel</span></div>
    <div class="tile"><div class="tile-icon">📝</div><b>Journal</b><span class="muted">Write thoughts and reflections</span></div>
    <div class="tile"><div class="tile-icon">📚</div><b>Learning</b><span class="muted">Track reading and learning time</span></div>
  </div>
</div>
</section>


<section id="learning" class="page">
<div class="inner lr-shell">
  <div class="lr-head">
    <div>
      <h1>📚 Learning Dashboard</h1>
      <p class="muted">Track skills, Python roadmap, practice, focus time, notes and reviews.</p>
    </div>
    <div class="lr-head-actions">
      <button class="lr-notes-launch" onclick="LR_openNotesPage()">📝 Take Notes</button>
      <button class="primary" onclick="LR_addSkill()">＋ Add Skill</button>
    </div>
  </div>

  <div class="lr-summary">
    <div><span>Active Skills</span><b id="lrActiveSkills">1</b><small>currently learning</small></div>
    <div><span>Total Learning</span><b id="lrTotalTime">0m</b><small>focus time recorded</small></div>
    <div><span>Topics Done</span><b id="lrTopicsDone">0</b><small>roadmap completed</small></div>
    <div><span>Current Streak</span><b id="lrStreak">0 days</b><small>consecutive learning days</small></div>
  </div>

  <div class="card">
    <div class="lr-section-head">
      <div><h2>🎓 My Skills</h2><p class="muted">Python is preloaded. Add SQL, JavaScript, Excel or any future skill.</p></div>
    </div>
    <div id="lrSkillCards" class="lr-skill-cards"></div>
  </div>

  <div class="card lr-overview">
    <div class="lr-overview-top">
      <div>
        <span class="lr-chip">CURRENT SKILL</span>
        <h2 id="lrSkillName">Python</h2>
        <p id="lrSkillDesc" class="muted"></p>
      </div>
      <div class="lr-progress-wrap">
        <div id="lrProgressCircle" class="lr-progress-circle"><span id="lrProgressPct">0%</span></div>
        <small>Roadmap complete</small>
      </div>
    </div>
    <div class="lr-overview-stats">
      <div><span>Completed</span><b id="lrCompleted">0 / 0</b></div>
      <div><span>Learning Time</span><b id="lrSkillTime">0m</b></div>
      <div><span>Practicing</span><b id="lrPracticing">0</b></div>
      <div><span>Review Due</span><b id="lrReviewDue">0</b></div>
    </div>
  </div>

  <div class="lr-two-col">
    <div class="card">
      <div class="lr-section-head"><div><h2>▶ Continue Learning</h2><p class="muted">Next unfinished topic.</p></div></div>
      <div id="lrContinue" class="lr-continue"></div>

      <div class="lr-section-head lr-mt">
        <div><h2>🎯 Today's Goal</h2><p class="muted">Small daily practice beats occasional long sessions.</p></div>
      </div>
      <div class="lr-goal-row">
        <input id="lrDailyGoal" type="number" min="5" step="5" value="30" onchange="LR_saveGoal(this.value)">
        <span>minutes</span>
        <button class="primary" onclick="LR_scheduleLearning()">Add to Time Planner</button>
      </div>
      <div id="lrTodayProgress" class="lr-today-progress"></div>
    </div>

    <div class="card">
      <div class="lr-section-head"><div><h2>✍️ What I Learned Today</h2><p class="muted">Write a short note in your own words.</p></div></div>
      <textarea id="lrTodayNote" class="lr-note" placeholder="Example: Learned lists, append(), slicing and solved 3 exercises..." oninput="LR_saveNote(this.value)"></textarea>
      <div class="lr-note-foot"><span id="lrNoteDate"></span><button class="secondary" onclick="LR_clearNote()">Clear</button></div>
    </div>
  </div>

  <div class="card">
    <div class="lr-section-head">
      <div><h2>🗺️ Python Roadmap</h2><p class="muted">Not Started → Learning → Practicing → Completed.</p></div>
      <div class="lr-filters">
        <button class="active" onclick="LR_setFilter('All',this)">All</button>
        <button onclick="LR_setFilter('Not Started',this)">Not Started</button>
        <button onclick="LR_setFilter('Learning',this)">Learning</button>
        <button onclick="LR_setFilter('Practicing',this)">Practicing</button>
        <button onclick="LR_setFilter('Completed',this)">Completed</button>
      </div>
    </div>
    <div id="lrRoadmap" class="lr-roadmap"></div>
  </div>

  <div class="lr-two-col">
    <div class="card">
      <div class="lr-section-head">
        <div><h2>🧪 Projects & Practice</h2><p class="muted">Use Python on practical tasks.</p></div>
        <button class="secondary" onclick="LR_addProject()">＋ Project</button>
      </div>
      <div id="lrProjects" class="lr-projects"></div>
    </div>

    <div class="card">
      <div class="lr-section-head"><div><h2>🔁 Review Due</h2><p class="muted">Revisit completed topics after a few days.</p></div></div>
      <div id="lrReviews"></div>
    </div>
  </div>

  <div class="card">
    <div class="lr-section-head"><div><h2>📈 Learning History</h2><p class="muted">Recent focus time and learning notes.</p></div></div>
    <div id="lrHistory"></div>
  </div>
</div>
</section>

<div id="lrNotesPage" class="lr-notes-page">
  <div class="lr-notes-topbar">
    <div class="lr-notes-top-left">
      <button class="secondary" onclick="LR_closeNotesPage()">← Back</button>
      <div>
        <h2>📝 My Learning Notes</h2>
        <p>Write freely, save notes, search them later, and create a backup anytime.</p>
      </div>
    </div>
    <div class="lr-notes-actions">
      <span id="lrNotesSaveState" class="lr-save-state">Saved</span>
      <span id="lrNotesCloudState" class="lr-cloud-state">☁ Sheet: checking...</span>
      <button class="secondary" onclick="LR_syncNotesFromSheet()">↻ Sync Sheet</button>
      <button class="secondary" onclick="LR_newNote()">＋ New Note</button>
      <button class="secondary" onclick="LR_exportNotesBackup()">⬇ Backup</button>
      <label class="secondary lr-import-label">⬆ Restore
        <input id="lrNotesImportInput" type="file" accept=".json,application/json" onchange="LR_importNotesBackup(this.files[0])">
      </label>
      <button class="primary" onclick="LR_saveCurrentNote(true)">💾 Save</button>
    </div>
  </div>

  <div class="lr-notes-layout">
    <aside class="lr-notes-sidebar">
      <div class="lr-notes-sidebar-head">
        <b>My Notes</b><span id="lrNotesCount">0</span>
      </div>
      <input id="lrNotesSearch" class="lr-notes-search" placeholder="Search notes..." oninput="LR_renderNotesList()">
      <div id="lrNotesList" class="lr-notes-list"></div>
    </aside>

    <main class="lr-notes-editor">
      <div class="lr-note-meta-row">
        <input id="lrFullNoteTitle" class="lr-full-note-title" placeholder="Note title..." oninput="LR_noteEditorChanged()">
        <select id="lrFullNoteSkill" onchange="LR_noteEditorChanged()"></select>
        <input id="lrFullNoteDate" type="date" onchange="LR_noteEditorChanged()">
      </div>

      <div class="lr-note-toolbar">
        <button onclick="LR_insertNoteText('• ')">• Bullet</button>
        <button onclick="LR_insertNoteText('1. ')">1. Number</button>
        <button onclick="LR_insertNoteText('✅ ')">✅ Done</button>
        <button onclick="LR_insertNoteText('❓ ')">❓ Question</button>
        <button onclick="LR_insertNoteText('💡 ')">💡 Idea</button>
        <button onclick="LR_insertNoteText('\\n---\\n')">— Divider</button>
      </div>

      <textarea id="lrFullNoteBody" class="lr-full-note-body"
        placeholder="Start writing your notes here..."
        oninput="LR_noteEditorChanged()"></textarea>

      <div class="lr-notes-footer">
        <span id="lrNotesWordCount">0 words</span>
        <span id="lrNotesLastSaved">Not saved yet</span>
      </div>
    </main>
  </div>
</div>

<section id="tasks" class="page"><div class="inner"><h1>✅ Tasks</h1><div class="card"><p class="muted">Tasks from your time blocks will be shown here.</p></div></div></section>
<section id="goals" class="page"><div class="inner"><h1>🎯 Goals</h1><div class="card"><p class="muted">Daily, weekly and monthly goals.</p></div></div></section>
<section id="analytics" class="page"><div class="inner"><h1>📊 Analytics</h1><div class="card"><p class="muted">Your productivity and money analytics will appear here.</p></div></div></section>


<section id="review" class="page">
  <div class="inner review-shell">

    <div class="review-header card">
      <div class="review-title-wrap">
        <h1>📔 Life Journal</h1>
        <p class="muted">One place for money, health, tasks and habits. Open any date to see the complete journal for that day.</p>
      </div>

      <div class="review-date-controls">
        <button class="secondary" onclick="RV_changeMonth(-1)">←</button>
        <select id="rvMonth" onchange="RV_renderAll()"></select>
        <select id="rvYear" onchange="RV_renderAll()"></select>
        <button class="secondary" onclick="RV_changeMonth(1)">→</button>
        <button class="secondary" onclick="RV_goCurrentMonth()">Current Month</button>
        <button class="secondary rv-sync-btn" onclick="RV_syncMoneySheet(true)">↻ Sync Sheet</button>
        <span id="rvSyncStatus" class="rv-sync-status">Not synced yet</span>
      </div>
    </div>

    <div class="review-summary-grid">
      <button class="rv-summary income" data-rv-metric="income" onclick="RV_selectMetric('income',this)">
        <span>⬇️ Total In</span><b id="rvIncome">₹0</b><small>Selected month only</small>
      </button>
      <button class="rv-summary expense" data-rv-metric="expense" onclick="RV_selectMetric('expense',this)">
        <span>⬆️ Total Out</span><b id="rvExpense">₹0</b><small>Selected month only</small>
      </button>
      <button class="rv-summary saving" data-rv-metric="saving" onclick="RV_selectMetric('saving',this)">
        <span>💰 Overall Remaining</span><b id="rvSaving">₹0</b><small>Cumulative up to month end</small>
      </button>
      <button class="rv-summary sleep" data-rv-metric="sleep" onclick="RV_selectMetric('sleep',this)">
        <span>😴 Sleep</span><b id="rvSleep">0h</b><small>Average per recorded night</small>
      </button>
      <button class="rv-summary task" data-rv-metric="done" onclick="RV_selectMetric('done',this)">
        <span>✅ Tasks Done</span><b id="rvTasksDone">0</b><small>Completed in month</small>
      </button>
      <button class="rv-summary pending" data-rv-metric="pending" onclick="RV_openRemainingTasksPopup()">
        <span>📌 Remaining Tasks</span><b id="rvTasksPending">0</b><small>Not Started + In Progress + Hold</small>
      </button>
      <button class="rv-summary calorie" data-rv-metric="calories" onclick="RV_selectMetric('calories',this)">
        <span>🍽️ Calories</span><b id="rvCalories">0</b><small>Average per recorded day</small>
      </button>
      <button class="rv-summary weight" data-rv-metric="weight" onclick="RV_selectMetric('weight',this)">
        <span>⚖️ Weight</span><b id="rvWeight">—</b><small>Latest reading in month</small>
      </button>
    </div>

    
    <div class="card" style="margin-top:14px"><div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><div><h2 style="margin:0">🔁 Habits</h2><p class="muted">Full tracker is in the Habits tab.</p></div><button onclick="showPage('habits',null);setTimeout(HB_renderAll,0)">Open Habits →</button></div></div>
<div class="rv-metric-filter card">
      <div>
        <b>Calendar View</b>
        <span id="rvMetricViewText">Overall — all tracked information</span>
      </div>
      <button class="active" data-rv-filter="all" onclick="RV_selectMetric('all',this)">Overall</button>
      <button data-rv-filter="income" onclick="RV_selectMetric('income',this)">Income</button>
      <button data-rv-filter="expense" onclick="RV_selectMetric('expense',this)">Expenses</button>
      <button data-rv-filter="saving" onclick="RV_selectMetric('saving',this)">Savings</button>
      <button data-rv-filter="sleep" onclick="RV_selectMetric('sleep',this)">Sleep</button>
      <button data-rv-filter="done" onclick="RV_selectMetric('done',this)">Tasks Done</button>
      <button data-rv-filter="pending" onclick="RV_selectMetric('pending',this)">Not Started</button>
      <button data-rv-filter="calories" onclick="RV_selectMetric('calories',this)">Calories</button>
      <button data-rv-filter="weight" onclick="RV_selectMetric('weight',this)">Weight</button>
    </div>

<div class="card rv-calendar-card" id="rvCalendarCard">
      <div class="rv-calendar-head">
        <div>
          <h2 id="rvCalendarTitle">Monthly Calendar</h2>
          <p class="muted">Each day shows the information already entered in Money, Health and Time. Click a date to review or add missing data.</p>
        </div>
        <div class="rv-legend">
          <span>💵 Income</span><span>💸 Expense</span><span>🏦 Savings</span>
          <span>😴 Sleep</span><span>✅ Done</span><span>📌 Pending</span>
          <span>🍽️ Calories</span><span>⚖️ Weight</span>
        </div>
      </div>

      <div class="rv-week-head">
        <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
      </div>
      <div id="rvCalendarGrid" class="rv-calendar-grid"></div>
    </div>

    <div class="card rv-trend-card">
      <div class="rv-calendar-head">
        <div>
          <h2>📊 Monthly Money Overview</h2>
          <p class="muted">Daily Income vs Expenses vs Savings for the selected month.</p>
        </div>
      </div>
      <div id="rvTrendBars" class="rv-trend-bars"></div>
    </div>
  </div>
</section>

<div id="rvDayModal" class="tools-modal" onclick="if(event.target===this)RV_closeDay()">
  <div class="modal-box rv-day-modal-box">
    <div class="modal-head">
      <div>
        <h2 id="rvDayTitle">Daily Journal</h2>
        <div id="rvDaySubtitle" class="muted"></div>
      </div>
      <button onclick="RV_closeDay()">✕</button>
    </div>

    <div id="rvDayBody"></div>

    <div class="rv-quick-entry-wrap">
      <h3>➕ Add Missing Information</h3>
      <p class="muted">Anything entered here is saved into the same Money / Health data used by the rest of your tracker.</p>

      <div class="rv-entry-tabs">
        <button class="active" onclick="RV_showEntryTab('money',this)">💸 Money</button>
        <button onclick="RV_showEntryTab('calories',this)">🍽️ Calories</button>
        <button onclick="RV_showEntryTab('weight',this)">⚖️ Weight</button>
        <button onclick="RV_showEntryTab('sleep',this)">😴 Sleep</button>
        <button onclick="RV_showEntryTab('tasks',this)">📌 Task</button>
      </div>

      <div id="rvEntryMoney" class="rv-entry-panel active">
        <div class="rv-entry-grid money">
          <label>Amount
            <input id="rvMoneyAmount" type="number" min="0" step="0.01" placeholder="0.00">
          </label>
          <label>Main Category
            <select id="rvMoneyMain" onchange="RV_updateMoneySubs()"></select>
          </label>
          <label>Sub Category
            <select id="rvMoneySub"></select>
          </label>
          <label>Account
            <select id="rvMoneyAccount"></select>
          </label>
          <label class="wide">Explanation
            <input id="rvMoneyExplanation" placeholder="What did you spend / receive?">
          </label>
          <button class="primary" onclick="RV_saveMoneyQuick()">Save Money Entry</button>
        </div>
      </div>

      <div id="rvEntryCalories" class="rv-entry-panel">
        <div class="rv-entry-grid">
          <label>Meal
            <select id="rvCalMeal"><option>Breakfast</option><option>Lunch</option><option>Dinner</option><option>Snacks</option></select>
          </label>
          <label>Food / Note
            <input id="rvCalFood" placeholder="Example: Dosa, lunch, tea">
          </label>
          <label>Calories
            <input id="rvCalValue" type="number" min="0" placeholder="0">
          </label>
          <button class="primary" onclick="RV_saveCaloriesQuick()">Save Calories</button>
        </div>
      </div>

      <div id="rvEntryWeight" class="rv-entry-panel">
        <div class="rv-entry-grid compact">
          <label>Weight (kg)
            <input id="rvWeightValue" type="number" min="1" step="0.1" placeholder="0.0">
          </label>
          <button class="primary" onclick="RV_saveWeightQuick()">Save Weight</button>
        </div>
      </div>

      <div id="rvEntrySleep" class="rv-entry-panel">
        <div class="rv-entry-grid compact">
          <label>Sleep Time
            <input id="rvSleepStart" type="time" value="23:00">
          </label>
          <label>Wake Time
            <input id="rvSleepEnd" type="time" value="06:00">
          </label>
          <button class="primary" onclick="RV_saveSleepQuick()">Save Sleep</button>
        </div>
      
      <div id="rvEntryTasks" class="rv-entry-panel">
        <div class="rv-entry-grid">
          <label>Task
            <input id="rvTaskTitle" placeholder="Task name">
          </label>
          <label>Minutes
            <input id="rvTaskMinutes" type="number" min="1" value="20">
          </label>
          <label>Status
            <select id="rvTaskStatus"><option>Not Started</option><option>In Progress</option><option>Done</option><option>Hold</option></select>
          </label>
          <button class="primary" onclick="RV_saveTaskQuick()">Save Task</button>
        </div>
      </div>
</div>
    </div>
  </div>
</div>


<section id="notes" class="page">
  <div class="inner">
    <div class="mt-notes-head">
      <div>
        <h1>📝 Notes</h1>
        <p class="muted">Notes are stored in the <b>Notes</b> tab of the same Google Sheet. Website ↔ Google Sheet sync.</p>
      </div>
      <button class="secondary" onclick="NT_loadNotes(true)">↻ Sync Sheet</button>
    </div>

    <div class="card mt-note-editor">
      <h2 id="ntEditorTitle">✍️ New Note</h2>
      <input type="hidden" id="ntId">
      <div class="mt-note-form">
        <label>Date
          <input type="date" id="ntDate">
        </label>
        <label>Title
          <input type="text" id="ntTitle" placeholder="Example: MeshWorks testing notes">
        </label>
        <label>Category
          <input type="text" id="ntCategory" list="ntCategoryList" placeholder="Work / Personal / Stock / Idea">
          <datalist id="ntCategoryList">
            <option value="Work"><option value="Personal"><option value="Stock">
            <option value="Idea"><option value="Learning"><option value="Important">
          </datalist>
        </label>
        <label>Status
          <select id="ntStatus">
            <option>Active</option>
            <option>Important</option>
            <option>Done</option>
            <option>Archived</option>
          </select>
        </label>
      </div>
      <label>Note
        <textarea id="ntBody" rows="7" placeholder="Write anything here..."></textarea>
      </label>
      <div class="mt-note-actions">
        <button class="primary" id="ntSaveBtn" onclick="NT_saveNote()">💾 Save Note</button>
        <button class="secondary" onclick="NT_clearEditor()">＋ New / Clear</button>
        <span id="ntStatusMsg" class="muted">Ready</span>
      </div>
    </div>

    <div class="card">
      <div class="mt-notes-toolbar">
        <div>
          <h2 style="margin:0">📚 My Notes</h2>
          <div id="ntCount" class="muted">0 notes</div>
        </div>
        <input id="ntSearch" type="search" placeholder="Search title, category or note..." oninput="NT_renderNotes()">
        <select id="ntFilter" onchange="NT_renderNotes()">
          <option value="ALL">All Categories</option>
        </select>
      </div>
      <div id="ntNotesList" class="mt-notes-list">
        <div class="muted">Open Notes to load from Google Sheet.</div>
      </div>
    </div>
  </div>
</section>

<section id="schedule" class="page">
<div class="inner">
  <div class="section-head">
    <div><h1>🗓️ Schedule</h1><p class="muted">Plan once in Daily view. Weekly and Monthly update automatically.</p></div>
    <button class="primary" onclick="SC_openEditor()">＋ Add Schedule</button>
  </div>

  <div class="card">
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <button id="scDailyBtn" class="primary" onclick="SC_setView('daily')">☀️ Daily</button>
      <button id="scWeeklyBtn" onclick="SC_setView('weekly')">📅 Weekly</button>
      <button id="scMonthlyBtn" onclick="SC_setView('monthly')">🗓️ Monthly</button>
      <input id="scDate" type="date" onchange="SC_render()" style="margin-left:auto">
      <label style="display:flex;align-items:center;gap:6px"><b>⏰ Wake up</b><input id="scWake" type="time" onchange="SC_saveWake();SC_render()"></label>
      <button onclick="SC_today()">Today</button>
    </div>
  </div>

  <div id="scDailyView" class="card" style="margin-top:12px"></div>
  <div id="scWeeklyView" class="card" style="margin-top:12px;display:none"></div>
  <div id="scMonthlyView" class="card" style="margin-top:12px;display:none"></div>
</div>

<div id="scEditor" class="tools-modal" style="display:none">
 <div class="modal-box" style="width:min(650px,96vw)">
  <div class="modal-head"><h2 id="scEditorTitle">Add Schedule</h2><button onclick="SC_closeEditor()">✕</button></div>
  <input id="scId" type="hidden">
  <div class="form-grid" style="margin-top:14px">
    <label><span>Date</span><input id="scEditDate" type="date"></label>
    <label><span>Title</span><input id="scTitle" placeholder="Morning routine / Work / Lunch"></label>
    <label><span>Start time</span><input id="scStart" type="time"></label>
    <label><span>End time</span><input id="scEnd" type="time"></label>
    <label><span>Type</span><select id="scType"><option>Personal</option><option>Work</option><option>Health</option><option>Learning</option><option>Family</option><option>Other</option></select></label>
    <label><span>Actual start</span><input id="scActualStart" type="time"></label>
    <label><span>Actual end</span><input id="scActualEnd" type="time"></label>
    <label><span>What actually happened?</span><input id="scActualTitle" placeholder="Leave blank if same as plan"></label>
    <label><span>Notes</span><input id="scNotes" placeholder="Optional"></label>
  </div>
  <div class="modal-actions">
    <button id="scDeleteBtn" style="display:none;margin-right:auto" onclick="SC_deleteCurrent()">🗑 Delete</button>
    <button onclick="SC_closeEditor()">Cancel</button>
    <button class="primary" onclick="SC_save()">Save</button>
  </div>
 </div>
</div>
</section>

<section id="habits" class="page">
<div class="inner">
  <div class="section-head">
    <div><h1>🔁 Habits</h1><p class="muted">Simple routine tracking — separate from Tasks and Time.</p></div>
    <button class="primary" onclick="HB_openEditor()">＋ Add Habit</button>
  </div>
  <div class="card">
    <div style="display:flex;align-items:end;gap:10px;flex-wrap:wrap;margin-bottom:14px">
      <label><span class="muted">Month</span><input id="hbMonth" type="month" onchange="HB_renderAll()"></label>
      <button onclick="HB_openCircular()">◯ Circular Tracker</button>
      <div id="hbSummary" class="muted" style="margin-left:auto"></div>
    </div>
    <div id="hbGrid"></div>
  </div>
</div>

<div id="hbEditor" class="tools-modal" style="display:none">
 <div class="modal-box" style="width:min(620px,96vw)">
  <div class="modal-head"><h2 id="hbEditorTitle">Add Habit</h2><button onclick="HB_closeEditor()">✕</button></div>
  <input id="hbId" type="hidden">
  <div class="form-grid" style="margin-top:14px">
   <label><span>Habit name</span><input id="hbName" placeholder="Walking"></label>
   <label><span>Frequency</span><select id="hbFrequency" onchange="HB_frequencyChanged()"><option>Daily</option><option>Weekly</option><option>Monthly</option></select></label>
   <label><span>Preferred time</span><input id="hbTime" type="time"></label>
   <label id="hbMonthDayWrap" style="display:none"><span>Day of month</span><input id="hbMonthDay" type="number" min="1" max="31" value="1"></label>
  </div>
  <div id="hbWeekWrap" style="display:none;margin-top:12px"><b>Repeat on</b><div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px">
   <label><input class="hbDow" type="checkbox" value="1"> Mon</label><label><input class="hbDow" type="checkbox" value="2"> Tue</label>
   <label><input class="hbDow" type="checkbox" value="3"> Wed</label><label><input class="hbDow" type="checkbox" value="4"> Thu</label>
   <label><input class="hbDow" type="checkbox" value="5"> Fri</label><label><input class="hbDow" type="checkbox" value="6"> Sat</label>
   <label><input class="hbDow" type="checkbox" value="0"> Sun</label>
  </div></div>
  <div class="modal-actions"><button onclick="HB_closeEditor()">Cancel</button><button class="primary" onclick="HB_saveHabit()">Save Habit</button></div>
 </div>
</div>

<div id="hbCircularModal" class="tools-modal" style="display:none">
 <div class="modal-box" style="width:min(850px,96vw)">
  <div class="modal-head"><h2>◯ Circular Habit Tracker</h2><button onclick="HB_closeCircular()">✕</button></div>
  <div id="hbCircularBody"></div>
 </div>
</div>
</section>

<section id="settings" class="page"><div class="inner"><h1>⚙️ Settings</h1><div class="card"><p class="muted">Tracker settings.</p></div></div></section>

</main>
</div>





<div id="moneyOthersWindow" class="upload-window">
  <div class="upload-window-box">
    <div class="upload-window-head">
      <div>
        <h2>🧰 Others</h2>
        <p class="muted">Money tools and additional options.</p>
      </div>
      <button class="upload-close" onclick="closeMoneyOthers()">✕</button>
    </div>

    <div class="upload-choice-grid">
      <button class="upload-choice" onclick="closeMoneyOthers();openUploadWindow()">
        <div class="upload-choice-icon">📤</div>
        <b>Upload Data</b>
        <span>Sheet upload or manual data entry</span>
      </button>

      <button class="upload-choice" onclick="closeMoneyOthers();openSheetDataWindow()">
        <div class="upload-choice-icon">📑</div>
        <b>Sheet Data</b>
        <span>View your imported sheet transactions</span>
      </button>

      <button class="upload-choice" onclick="closeMoneyOthers();openViewOptions()">
        <div class="upload-choice-icon">👁️</div>
        <b>View Options</b>
        <span>View all, income, expenses, savings and loans</span>
      </button>

      <button class="upload-choice danger-choice" onclick="closeMoneyOthers();clearAllMoneyData()">
        <div class="upload-choice-icon">🗑️</div>
        <b>All Clear</b>
        <span>Clear all money transaction data</span>
      </button>

      <button class="upload-choice" onclick="closeMoneyOthers();openMoneySet()">
        <div class="upload-choice-icon">⚙️</div>
        <b>Set</b>
        <span>Edit main categories, sub categories and accounts</span>
      </button>
    </div>
  </div>
</div>


<div id="moneySetWindow" class="upload-window">
  <div class="upload-window-box">
    <div class="upload-window-head">
      <div>
        <h2>⚙️ Money Set</h2>
        <p class="muted">Edit your master categories. Changes here update Manual Entry and future website classification.</p>
      </div>
      <button class="upload-close" onclick="closeMoneySet()">✕</button>
    </div>

    <div class="note">
      Categories and sub categories are linked with the Google Sheet tab <b>help</b>.
      Changes made here are saved back to <b>help</b>; changes made in <b>help</b> are loaded into the website on sync.
    </div>
    <div id="moneySetSyncStatus" class="muted" style="margin:10px 2px 4px">Help sheet not synced yet.</div>

    <div id="moneySetBody"></div>

    <div class="card">
      <h3>＋ Add New Main Category</h3>
      <div class="add-row">
        <input id="newMainCategoryName" placeholder="Example: Insurance">
        <button onclick="addMainCategory()">＋ Add</button>
      </div>
    </div>

    <div class="card">
      <h3>🏦 Accounts</h3>
      <div id="setAccountsBody"></div>
      <div class="add-row">
        <input id="setNewAccount" placeholder="Add new account">
        <button onclick="setAddAccount()">＋ Add</button>
      </div>
    </div>
  </div>
</div>

<div id="viewOptionsWindow" class="upload-window">
  <div class="upload-window-box view-window-box">
    <div class="upload-window-head">
      <div>
        <h2>👁️ View Options</h2>
        <p class="muted">Choose the type of money report you want.</p>
      </div>
      <button class="upload-close" onclick="closeViewOptions()">✕</button>
    </div>

    <div id="viewModeChooser" class="upload-choice-grid view-mode-square-grid">
      <button class="upload-choice view-mode-square" onclick="openViewMode1()">
        <div class="upload-choice-icon">🧮</div>
        <b>Overall Transactions</b>
        <span>See cumulative totals for every category and sub category — Overall, Yearly, Monthly, Weekly or Daily.</span>
      </button>

      <button class="upload-choice view-mode-square" onclick="openViewMode2()">
        <div class="upload-choice-icon">📒</div>
        <b>Passbook Transactions</b>
        <span>Daily, Monthly and Yearly cash-flow passbook with cumulative balance.</span>
      </button>

      <button class="upload-choice view-mode-square" onclick="openViewMode3()">
        <div class="upload-choice-icon">🔎</div>
        <b>Period Summary</b>
        <span>Daily, Monthly and Yearly summary like your Google Sheet with Income, Expenses, Saving, Others and Remaining Amount.</span>
      </button>

      <button class="upload-choice view-mode-square" onclick="openViewMode4()">
        <div class="upload-choice-icon">🏦</div>
        <b>Bank Wise</b>
        <span>Cross-check Axis, Wallet, IOB and every account. See cash balance, active savings such as F/D, and all transactions.</span>
      </button>
      <button class="upload-choice view-mode-square" onclick="openViewMode5()">
        <div class="upload-choice-icon">🏠</div>
        <b>Room</b>
        <span>Sharing and Gifts. Keep shared-expense splitting separate from person-wise gift tracking.</span>
      </button>

      <button class="upload-choice view-mode-square" onclick="openViewMode6()">
        <div class="upload-choice-icon">💡</div>
        <b>Money Insights</b>
        <span>See where money is going, what increased, savings rate, outstanding loans, free cash and monthly budget targets.</span>
      </button>
    </div>

    <div id="viewModeContent"></div>
  </div>
</div>
</div>

<div id="sheetDataWindow" class="upload-window">
  <div class="upload-window-box">
    <div class="upload-window-head">
      <div>
        <h2>📑 Sheet Data</h2>
        <p class="muted">Imported transactions are shown only here.</p>
      </div>
      <button class="upload-close" onclick="closeSheetDataWindow()">✕</button>
    </div>
    <div id="sheetDataStatus" class="note">No sheet imported yet.</div>
    <div id="sheetDataTable"></div>
  </div>
</div>


<div id="moneyCategoryTransactionsWindow" class="upload-window">
  <div class="upload-window-box category-transactions-box">
    <div class="upload-window-head">
      <div>
        <h2 id="moneyCategoryTransactionsTitle">Transactions</h2>
        <p id="moneyCategoryTransactionsSummary" class="muted"></p>
      </div>
      <button class="upload-close" onclick="closeMoneyCategoryTransactions()">✕</button>
    </div>

    <div id="moneySubcategoryTabs" class="subcategory-tabs"></div>

    <div class="category-filter-bar">
      <input id="moneyCategorySearch" placeholder="Search sub category, explanation or account..." oninput="renderMoneyCategoryTransactions()">
    </div>

    <div id="moneyCategoryTransactionsTable"></div>
  </div>
</div>


<div id="moneyForecastWindow" class="upload-window">
  <div class="upload-window-box forecast-window-box">
    <div class="upload-window-head">
      <div>
        <h2>🔮 Money Forecast</h2>
        <p class="muted">Estimate next month's cash position and how much you can safely spend.</p>
      </div>
      <button class="upload-close" onclick="closeMoneyForecast()">✕</button>
    </div>

    <div class="forecast-toolbar card">
      <label>Forecast Month
        <input id="forecastMonth" type="month" onchange="renderMoneyForecast()">
      </label>
      <label>Minimum Reserve
        <input id="forecastReserve" type="number" min="0" step="100" value="50000" oninput="renderMoneyForecast()">
      </label>
      <label>Average Based On
        <select id="forecastLookback" onchange="renderMoneyForecast()">
          <option value="3" selected>Last 3 months</option>
          <option value="6">Last 6 months</option>
          <option value="12">Last 12 months</option>
        </select>
      </label>
    </div>

    <div class="forecast-kpi-grid">
      <div class="forecast-kpi current">
        <span>Current Cash Balance</span>
        <b id="forecastCurrentBalance">₹0.00</b>
      </div>
      <div class="forecast-kpi freecash">
        <span>Monthly Free Cash</span>
        <b id="forecastFreeCash">₹0.00</b>
      </div>
      <div class="forecast-kpi safe">
        <span>Safe to Spend</span>
        <b id="forecastSafeSpend">₹0.00</b>
      </div>
      <div class="forecast-kpi end">
        <span>Projected End Balance</span>
        <b id="forecastEndBalance">₹0.00</b>
      </div>
    </div>

    <div id="forecastDecision" class="forecast-decision"></div>

    <div class="forecast-columns">
      <div class="card">
        <h3>Expected Next Month</h3>
        <p class="muted">Values are auto-filled from your recent history. You can change them.</p>

        <div class="forecast-input-grid">
          <label>Income
            <input id="fcIncome" type="number" step="1" oninput="recalculateForecastFromInputs()">
          </label>
          <label>Needs
            <input id="fcNeeds" type="number" step="1" oninput="recalculateForecastFromInputs()">
          </label>
          <label>Wants
            <input id="fcWants" type="number" step="1" oninput="recalculateForecastFromInputs()">
          </label>
          <label>Planned Savings
            <input id="fcSavings" type="number" step="1" oninput="recalculateForecastFromInputs()">
          </label>
          <label>Loan In
            <input id="fcLoanIn" type="number" step="1" oninput="recalculateForecastFromInputs()">
          </label>
          <label>Loan Out / Repayment
            <input id="fcLoanOut" type="number" step="1" oninput="recalculateForecastFromInputs()">
          </label>
        </div>

        <div class="note" style="margin-top:10px">
          Internal Transfer In/Out is excluded from the overall forecast because it only moves your own money between accounts.
        </div>
      </div>

      <div class="card">
        <h3>How the forecast is calculated</h3>
        <table class="forecast-formula-table">
          <tr><td>Starting cash</td><td id="fcFormulaStart">₹0.00</td></tr>
          <tr><td>+ Income</td><td id="fcFormulaIncome">₹0.00</td></tr>
          <tr><td>+ Loan In</td><td id="fcFormulaLoanIn">₹0.00</td></tr>
          <tr><td>− Needs</td><td id="fcFormulaNeeds">₹0.00</td></tr>
          <tr><td>− Wants</td><td id="fcFormulaWants">₹0.00</td></tr>
          <tr><td>− Savings</td><td id="fcFormulaSavings">₹0.00</td></tr>
          <tr><td>− Loan Out</td><td id="fcFormulaLoanOut">₹0.00</td></tr>
          <tr class="report-total"><td>Projected End Balance</td><td id="fcFormulaEnd">₹0.00</td></tr>
        </table>
      </div>
    </div>

    <div class="card">
      <h3>Recent Monthly Pattern</h3>
      <div id="forecastHistoryTable"></div>
    </div>
  </div>
</div>


<div id="option1TransactionPopup" class="upload-window">
  <div class="upload-window-box option1-popup-box">
    <div class="upload-window-head">
      <div>
        <h2 id="option1PopupTitle">Transactions</h2>
        <p id="option1PopupSummary" class="muted"></p>
      </div>
      <button class="upload-close" onclick="closeOption1TransactionPopup()">✕</button>
    </div>

    <div class="option1-popup-filter">
      <input id="option1PopupSearch"
             placeholder="Search date, sub category, explanation or account..."
             oninput="renderOption1TransactionPopup()">
    </div>

    <div id="option1PopupTable"></div>
  </div>
</div>

<div id="uploadWindow" class="upload-window">
  <div class="upload-window-box">
    <div class="upload-window-head">
      <div>
        <h2>📤 Add Money Data</h2>
        <p class="muted">Choose how you want to add money data.</p>
      </div>
      <button class="upload-close" onclick="closeUploadWindow()">✕</button>
    </div>

    <div id="uploadChoiceArea" class="upload-choice-grid">
      <button class="upload-choice" onclick="showUploadSheetInsideWindow()">
        <div class="upload-choice-icon">📊</div>
        <b>Sheet Upload</b>
        <span>Upload your Google Sheet, Excel or CSV data.</span>
      </button>

      <button class="upload-choice" onclick="showManualInsideWindow()">
        <div class="upload-choice-icon">✍️</div>
        <b>Manual Data Entry</b>
        <span>Enter a transaction manually.</span>
      </button>
    </div>

    <div id="uploadWindowContent"></div>
  </div>
</div>


<div id="accountBalanceModal" class="tools-modal" onclick="if(event.target===this)closeAccountBalancePopup()">
  <div class="modal-box account-balance-modal-box">
    <div class="modal-head">
      <div>
        <h2 style="margin:0">💰 Account Balances</h2>
        <div class="muted" style="margin-top:4px">Remaining cash balance grouped by account.</div>
      </div>
      <button onclick="closeAccountBalancePopup()">✕</button>
    </div>

    <div id="accountBalanceTotal" class="account-balance-total"></div>
    <div id="accountBalanceList" class="account-balance-list"></div>

    <div class="account-balance-note">
      Balance = Income + Transfer In + Loan In + Savings Return − Expenses − Savings − Transfer Out − Loan Out.
    </div>
  </div>
</div>


<div id="tbStatusDetailsModal" class="tools-modal" onclick="if(event.target===this)TB_closeStatusDetails()">
  <div class="modal-box tb-status-details-box">
    <div class="modal-head">
      <div>
        <h2 id="tbStatusDetailsTitle" style="margin:0">📌 Task Details</h2>
        <div id="tbStatusDetailsSubtitle" class="muted" style="margin-top:4px"></div>
      </div>
      <button onclick="TB_closeStatusDetails()">✕</button>
    </div>

    <div id="tbStatusDetailsSummary" class="tb-status-details-summary"></div>
    <div id="tbStatusDetailsTable" class="tb-status-details-table"></div>
  </div>
</div>


<div id="tbRecurringDetailsModal" class="tools-modal" onclick="if(event.target===this)TB_closeRecurringDetails()">
  <div class="modal-box tb-recurring-details-box">
    <div class="modal-head">
      <div>
        <h2 id="tbRecurringDetailsTitle" style="margin:0">🔁 Recurring Tasks</h2>
        <div id="tbRecurringDetailsSub" class="muted" style="margin-top:4px"></div>
      </div>
      <button onclick="TB_closeRecurringDetails()">✕</button>
    </div>
    <div id="tbRecurringDetailsBody"></div>
  </div>
</div>


<div id="tbTaskEditorModal" class="tools-modal" onclick="if(event.target===this)TB_closeTaskEditor()">
  <div class="modal-box tb-task-editor-box">
    <div class="modal-head">
      <div><h2 style="margin:0">✏️ Edit Task</h2><div class="muted" style="margin-top:4px">Edit this time block directly.</div></div>
      <button onclick="TB_closeTaskEditor()">✕</button>
    </div>
    <input id="tbEditTaskId" type="hidden">
    <div class="tb-task-editor-grid">
      <label>Task<input id="tbEditTitle"></label>
      <label>Priority<input id="tbEditPriority" type="number" min="1"></label>
      <label>Start<input id="tbEditStart" type="time"></label>
      <label>Minutes<input id="tbEditDuration" type="number" min="20" step="20"></label>
      <label>Date<input id="tbEditDate" type="date"></label>
      <label>Type<select id="tbEditType"><option>Job</option><option>Personal</option><option>Money</option><option>Health</option><option>Learning</option><option>Other</option></select></label>
      <label>Status<select id="tbEditStatus"><option>Not Started</option><option>In Progress</option><option>Done</option><option>Hold</option></select></label>
    </div>
    <div class="tb-task-editor-actions">
      <button class="primary" onclick="TB_saveTaskEditor()">💾 Save Changes</button>
      <button class="start" onclick="TB_editorQuickStatus('In Progress')">▶ Start</button>
      <button class="done" onclick="TB_editorQuickStatus('Done')">✓ Done</button>
      <button class="hold" onclick="TB_editorQuickStatus('Hold')">⏸ Hold</button>
      <button class="delete" onclick="TB_editorDeleteTask()">🗑 Delete</button>
    </div>
    <div id="tbEditTimestampInfo" class="tb-edit-timestamp-info"></div>
  </div>
</div>

<div id="toolsModal" class="tools-modal">
<div class="modal-box">
<div class="modal-head"><h2>⚙️ Money Tools</h2><button onclick="closeTools()">✕</button></div>
<p class="muted">Add or remove categories and accounts. These lists control the Manual Data Entry dropdowns.</p>
<div id="toolsBody"></div>
<div class="actions"><button class="secondary" onclick="closeTools()">Done</button></div>
</div>
</div>

<script>var RV_selectedDate="";
var RV_selectedMetric="all";
var RV_reviewInitialized=false;
var RV_sheetSyncInProgress=false;


const defaultConfig={
categories:{
Income:["Rahavan salary","Priyanka salary","Dividend","Interest - F/D","coins","Lend Borrowed money given (repayment)","Money got as a gift","Bank mini balance interest","Money borrowed want to return","Money got as a gift want to resend it again one day","F/D After maturity","gold loan"],
Needs:["Rent","Service","Medical","Groceries","zepto","Recharge","Petrol","Travel","Money lent","Milk","Veg","Current Bill","Gas","Money sended as a gift","egg","water","pooja","oil","borrowed Lend Borrowed money given (repayment)","money resended which has been brought as gift","Borrowed Money given","ATM"],
Savings:["Gold","F/D","PPF","stocks"],
Others:["priyanka actual salary"],
In:["Transfer In"],
Wants:["Don't know","Things","Non-Veg","Dress","Fruits","Hotel","Movie","Snacks","Hair cutting","Tea"],
Out:["Transfer out"],
"Loan I Took":["Loan received","Loan repayment paid"],
"Loan I Gave":["Money lent","Loan repayment received"],
"Savings Return":["F/D Maturity","PPF Withdrawal","Gold Sale","Stock Withdrawal"]
},
accounts:["Axis","joint axis","wallet","iob","state","ib","icici priyanka"]
};

let config=JSON.parse(localStorage.getItem("moneyConfig")||"null")||defaultConfig;
let timeBlocks=JSON.parse(localStorage.getItem("timeBlocks")||"[]");

function startApp(){
  const welcome=document.getElementById("welcome");
  const app=document.getElementById("app");

  if(welcome){
    welcome.classList.add("force-hidden");
    welcome.style.display="none";
  }

  if(app){
    app.classList.add("force-visible");
    app.style.display="block";
  }

  document.querySelectorAll(".page").forEach(function(p){
    p.classList.remove("active");
  });

  const dashboard=document.getElementById("dashboard");
  if(dashboard){
    dashboard.classList.add("active");
  }

  document.querySelectorAll(".sidebar .nav").forEach(function(n){
    n.classList.remove("active");
  });

  const firstNav=document.querySelector(".sidebar .nav");
  if(firstNav)firstNav.classList.add("active");

  // Persist that the user has entered the app in this browser session.
  try{sessionStorage.setItem("myTrackingStarted","1");}catch(e){}

  // Render sections that have live summary content.
  try{
    if(typeof updateDashboard==="function")updateDashboard();
  }catch(e){}
}


function clearStockMarketArea(){
  const area=document.getElementById("stockMarketArea");
  if(area)area.innerHTML="";
}


function clearStockMarketArea(){
  const area=document.getElementById("stockMarketArea");
  if(area)area.innerHTML="";
}

function openNiftyHeatmap(){
  const area=document.getElementById("stockMarketArea");
  if(!area)return;

  area.innerHTML=
    '<div class="card market-panel">'+
      '<div class="market-head">'+
        '<div><h2>🟩 NIFTY 50 Heatmap</h2>'+
        '<p class="muted">The ChatGPT preview blocks embedded live-market widgets. Use the button below to open the live heatmap directly.</p></div>'+
        '<button class="secondary" onclick="clearStockMarketArea()">Close</button>'+
      '</div>'+
      '<div class="market-safe-box">'+
        '<div class="big-market-icon">🟩🟥</div>'+
        '<h3>Live NIFTY 50 Heatmap</h3>'+
        '<p>Green = stock is up today<br>Red = stock is down today</p>'+
        '<button class="primary" onclick="window.open(\'https://www.tradingview.com/heatmap/stock/?color=change&dataset=NIFTY50&group=sector&size=market_cap_basic\',\'_blank\')">Open Live Heatmap</button>'+
      '</div>'+
    '</div>';

  area.scrollIntoView({behavior:"smooth",block:"start"});
}

function openAllNseStocks(){
  const area=document.getElementById("stockMarketArea");
  if(!area)return;

  area.innerHTML=
    '<div class="card market-panel">'+
      '<div class="market-head">'+
        '<div><h2>🏛️ All NSE Stocks</h2>'+
        '<p class="muted">The preview cannot safely embed the live NSE screener. Open the full live market list in a new browser tab.</p></div>'+
        '<button class="secondary" onclick="clearStockMarketArea()">Close</button>'+
      '</div>'+
      '<div class="market-safe-box">'+
        '<div class="big-market-icon">📊</div>'+
        '<h3>Live NSE Stock Screener</h3>'+
        '<p>View listed NSE stocks, latest available price, daily % change and green/red movement.</p>'+
        '<button class="primary" onclick="window.open(\'https://www.tradingview.com/markets/stocks-india/market-movers-all-stocks/\',\'_blank\')">Open All NSE Stocks</button>'+
      '</div>'+
    '</div>';

  area.scrollIntoView({behavior:"smooth",block:"start"});
}



let googleSheetConnected = false;
let googleSyncTimer = null;

function setGoogleSyncStatus(text, ok){
  const el=document.getElementById("googleSyncStatus");
  if(!el)return;
  el.textContent=text;
  el.style.color=ok===true?"#15803d":ok===false?"#dc2626":"#667085";
}

function googleSheetDateToDisplay(value){
  if(value===null || value===undefined || value==="")return "";

  const s=String(value).trim();

  // Google Sheet sends the exact displayed DD-MM-YYYY value.
  let m=s.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
  if(m){
    return String(m[1]).padStart(2,"0")+"-"+String(m[2]).padStart(2,"0")+"-"+m[3];
  }

  // Support ISO only when explicitly received.
  m=s.match(/^(\d{4})-(\d{2})-(\d{2})(?:T.*)?$/);
  if(m){
    return m[3]+"-"+m[2]+"-"+m[1];
  }

  // Never ask JavaScript to guess an ambiguous date.
  return s;
}
function normalizeGoogleRow(row){
  return {
    source:"google-sheet",
    sheetRow:Number(row["__rowNumber"]||0),
    date:googleSheetDateToDisplay(row["Date"]||row["date"]||""),
    day:row["Day"]||row["day"]||"",
    mainCategory:row["Main Category"]||row["main category"]||row["MainCategory"]||"",
    subCategory:row["sub category"]||row["Sub Category"]||row["subcategory"]||"",
    explanation:row["Explanation"]||row["explanation"]||"",
    amount:Number(String(row["Amount"]||row["amount"]||0).replace(/,/g,""))||0,
    account:row["spend on which account"]||row["Amount spend on which account"]||row["Account"]||row["account"]||"",
    remainingAmountRaw:row["Remaining amount"]!==undefined ? row["Remaining amount"] : row["Remaining Amount"],
    overallRemainingRaw:row["over all remaining amount"]!==undefined ? row["over all remaining amount"] : (row["Overall Remaining Amount"]!==undefined ? row["Overall Remaining Amount"] : row["Overall Remaining"]),
    remainingAmount:Number(String(row["Remaining amount"]!==undefined ? row["Remaining amount"] : (row["Remaining Amount"]||0)).replace(/,/g,""))||0,
    overallRemaining:Number(String(row["over all remaining amount"]!==undefined ? row["over all remaining amount"] : (row["Overall Remaining Amount"]!==undefined ? row["Overall Remaining Amount"] : (row["Overall Remaining"]||0))).replace(/,/g,""))||0,
    order:Number(String(row["order"]||row["Order"]||0).replace(/,/g,""))||0,
    sharing:String(row["Sharing"]||row["sharing"]||"").trim(),
    accountBalanceCheckpoint:row["Account Balance Checkpoint"]===true || String(row["Account Balance Checkpoint"]||"").toLowerCase()==="true",
    hBackground:String(row["H Background"]||"").trim()
  };
}


function sheetMoneyNumber(v){
  if(v===null || v===undefined || v==="") return null;
  const s=String(v).replace(/[₹,\s]/g,"").trim();
  if(!s) return null;
  const n=Number(s);
  return Number.isFinite(n) ? n : null;
}

function syncFromGoogleSheet(showMessage){
  return new Promise((resolve,reject)=>{
    setGoogleSyncStatus("Syncing ALL rows from website sheet...",null);

    google.script.run
      .withSuccessHandler(function(result){
        try{
          if(!result || !result.success){
            throw new Error((result && result.message) || "Apps Script returned an error.");
          }

          const raw=result.data||[];
          const rows=raw.map(normalizeGoogleRow).filter(function(r){
            const exists=!!r.date && !!r.account && Number(r.amount||0)!==0;
            const h=r.remainingAmountRaw;
            const completed=!(h==="" || h===null || h===undefined);
            return exists && completed;
          });

          // STRICT MASTER: Google Sheet is the ONLY source of transactions.
          // Any old local-only/pending transaction is discarded.
          localStorage.setItem("moneyEntries",JSON.stringify(rows));
          localStorage.setItem("lastGoogleSync",new Date().toISOString());

          const validDates=rows
            .map(function(r){return parseTrackerDate(r.date);})
            .filter(Boolean)
            .sort(function(a,b){return a-b;});

          const firstDate=validDates.length?displayTrackerDate(validDates[0]):"—";
          const lastDate=validDates.length?displayTrackerDate(validDates[validDates.length-1]):"—";

          const diagnostics={
            loaded:rows.length,
            backendReturned:raw.length,
            sheetLastRow:Number(result.sheetLastRow||0),
            firstDataRow:Number(result.firstDataRow||2),
            lastDataRow:Number(result.lastDataRow||0),
            firstDate:firstDate,
            lastDate:lastDate
          };
          localStorage.setItem("lastGoogleSyncDiagnostics",JSON.stringify(diagnostics));

          if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();

          if(typeof syncMoneySetFromGoogleSheet==="function"){
            syncMoneySetFromGoogleSheet(false).catch(function(){});
          }

          googleSheetConnected=true;

          const diagText="Connected ✓ — "+rows.length+" transactions"+
            (diagnostics.sheetLastRow?(" · sheet last row "+diagnostics.sheetLastRow):"")+
            " · "+firstDate+" → "+lastDate;

          setGoogleSyncStatus(diagText,true);

          const rv=document.getElementById("rvSyncStatus");
          if(rv){
            rv.textContent="✓ "+rows.length+" transactions · "+firstDate+" → "+lastDate;
            rv.className="rv-sync-status ok";
          }

          if(showMessage){
            alert(
              "✓ Full Google Sheet sync completed.\n\n"+
              "Transactions loaded: "+rows.length+"\n"+
              "Sheet last row: "+diagnostics.sheetLastRow+"\n"+
              "Date range: "+firstDate+" → "+lastDate
            );
          }

          resolve(rows);
        }catch(err){
          setGoogleSyncStatus("Sync failed: "+err.message,false);
          if(showMessage)alert("Google Sheet sync failed.\n"+err.message);
          reject(err);
        }
      })
      .withFailureHandler(function(err){
        const msg=(err&&err.message)?err.message:String(err);
        setGoogleSyncStatus("Sync failed: "+msg,false);
        if(showMessage)alert("Google Sheet sync failed.\n"+msg);
        reject(err);
      })
      .getTransactionsForWeb();
  });
}

async function connectGoogleSheet(){
  const status=document.getElementById("googleSyncStatus");
  if(status)status.textContent="Connecting to Google Sheet...";

  try{
    await syncFromGoogleSheet(false);
    googleSheetConnected=true;

    // V156: No automatic Google Sheet refresh while typing.
    // Google Sheet -> Website is manual through Sync/Refresh only.

    alert("✓ Google Sheet connected and money data loaded.");
  }catch(err){
    googleSheetConnected=false;
    if(status)status.textContent="Connection failed — click Connect & Load again";
  }
}

function addTransactionToGoogleSheet(entry){
  return new Promise((resolve,reject)=>{
    google.script.run
      .withSuccessHandler(function(result){
        if(result && result.success && result.sheetSaved) resolve(result);
        else reject(new Error((result && result.message) || "Could not save transaction."));
      })
      .withFailureHandler(function(err){
        reject(err);
      })
      .addTransactionForWeb(entry);
  });
}

let moneySetSaveTimer=null;

function setMoneySetSyncStatus(text,ok){
  const el=document.getElementById("moneySetSyncStatus");
  if(!el)return;
  el.textContent=text;
  el.style.color=ok===true?"#15803d":ok===false?"#dc2626":"#667085";
}

function syncMoneySetFromGoogleSheet(showMessage){
  return new Promise((resolve,reject)=>{
    setMoneySetSyncStatus("Loading categories from help sheet...",null);

    google.script.run
      .withSuccessHandler(function(result){
        if(!result || !result.success){
          const msg=(result && result.message) || "Could not read help sheet.";
          setMoneySetSyncStatus("Help sync failed: "+msg,false);
          if(showMessage)alert(msg);
          reject(new Error(msg));
          return;
        }

        const categories=result.categories||{};
        config.subCategoryMainMap=result.subCategoryMainMap||{};
        if(Object.keys(categories).length){
          config.categories=categories;
          localStorage.setItem("moneyConfig",JSON.stringify(config));
          if(document.getElementById("moneyQuickEntry"))renderMoneyQuickEntry();

          if(openMoneySetCategory && !config.categories[openMoneySetCategory]){
            openMoneySetCategory=Object.keys(config.categories)[0]||"";
          }

          const win=document.getElementById("moneySetWindow");
          if(win && win.style.display==="flex")renderMoneySet();
        }

        setMoneySetSyncStatus(
          "Help sheet synced ✓ — "+Object.keys(config.categories).length+" main categories",
          true
        );

        if(showMessage)alert("✓ Money Set loaded from the help sheet.");
        resolve(categories);
      })
      .withFailureHandler(function(err){
        const msg=(err && err.message)?err.message:String(err);
        setMoneySetSyncStatus("Help sync failed: "+msg,false);
        if(showMessage)alert("Help sheet sync failed.\n"+msg);
        reject(err);
      })
      .getMoneySetForWeb();
  });
}

function pushMoneySetToGoogleSheet(){
  setMoneySetSyncStatus("Saving Money Set to help sheet...",null);

  google.script.run
    .withSuccessHandler(function(result){
      if(result && result.success){
        setMoneySetSyncStatus("Saved to help sheet ✓",true);
      }else{
        setMoneySetSyncStatus("Save failed: "+((result&&result.message)||"Unknown error"),false);
      }
    })
    .withFailureHandler(function(err){
      const msg=(err&&err.message)?err.message:String(err);
      setMoneySetSyncStatus("Save failed: "+msg,false);
    })
    .saveMoneySetForWeb(config.categories);
}



/* ============================================================
   V72 SMART DAILY PLANNER
   ============================================================ */
const TB_TASK_KEY="tbTasksV2";
const TB_SLOT_KEY="tbSlotsV2";
const TB_FOCUS_KEY="tbFocusLogV2";
const TB_RECUR_KEY="tbRecurringV2";
const TB_RECUR_STATUS_KEY="tbRecurringStatusV1";
const TB_RECUR_BRAIN_KEY="tbRecurringBrainV1";
const TB_RECUR_DELETED_OCC_KEY="tbRecurringDeletedOccurrenceV1";
const TB_BRAIN_KEY="tbBrainDumpV1";
const TB_DELETED_TASK_KEY="tbDeletedPlanningTasksV1";

let TB_timerDefaultSeconds=20*60;
let TB_timerSeconds=TB_timerDefaultSeconds;
let TB_timerInterval=null;
let TB_timerRunning=false;

function TB_todayKey(){
  const d=new Date();
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
}
let TB_selectedDate=TB_todayKey();

function TB_dateObj(k){return new Date(k+"T00:00:00")}
function TB_fmtDate(k){return TB_dateObj(k).toLocaleDateString("en-IN",{weekday:"long",day:"2-digit",month:"long",year:"numeric"})}
function TB_loadTasks(){try{return JSON.parse(localStorage.getItem(TB_TASK_KEY)||"[]")}catch(e){return[]}}
function TB_saveTasks(v){localStorage.setItem(TB_TASK_KEY,JSON.stringify(v))}
function TB_loadSlots(){try{return JSON.parse(localStorage.getItem(TB_SLOT_KEY)||"{}")}catch(e){return{}}}
function TB_saveSlots(v){localStorage.setItem(TB_SLOT_KEY,JSON.stringify(v))}
function TB_loadFocus(){try{return JSON.parse(localStorage.getItem(TB_FOCUS_KEY)||"[]")}catch(e){return[]}}
function TB_saveFocus(v){localStorage.setItem(TB_FOCUS_KEY,JSON.stringify(v))}
function TB_loadRecurring(){try{return JSON.parse(localStorage.getItem(TB_RECUR_KEY)||"[]")}catch(e){return[]}}
function TB_saveRecurring(v){localStorage.setItem(TB_RECUR_KEY,JSON.stringify(v))}

function TB_seedTasksIfNeeded(){
  if(TB_loadTasks().length)return;
  const a=[];for(let i=0;i<10;i++)a.push({id:"tb-"+Date.now()+"-"+i,priority:"",title:"",type:"Job",estimate:20,startTime:"",planDate:TB_todayKey(),status:"Not Started",completedDate:"",actualMinutes:0});
  TB_saveTasks(a);
}
function TB_seedRecurringIfNeeded(){
  if(TB_loadRecurring().length)return;
  TB_saveRecurring([
    {id:"r-rent",title:"Pay Rent",kind:"Monthly",day:2,date:"",weekday:1,start:"08:00",minutes:20,type:"Money",active:true},
    {id:"r-eb",title:"Pay EB Bill",kind:"Monthly",day:5,date:"",weekday:1,start:"08:00",minutes:20,type:"Money",active:true},
    {id:"r-wifi",title:"Pay WiFi Bill",kind:"Monthly",day:16,date:"",weekday:1,start:"08:00",minutes:20,type:"Money",active:true},
    {id:"r-walk",title:"Walking",kind:"Daily",day:1,date:"",weekday:1,start:"06:20",minutes:60,type:"Health",active:true},
    {id:"r-gym",title:"Gym",kind:"Daily",day:1,date:"",weekday:1,start:"18:00",minutes:120,type:"Health",active:true}
  ]);
}

function TB_setPlanDate(v){if(!v)return;TB_selectedDate=v;TB_renderAll();setTimeout(TB_scrollToNow,50)}
function TB_changePlanDate(n){const d=TB_dateObj(TB_selectedDate);d.setDate(d.getDate()+n);TB_setPlanDate(d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0"))}
function TB_goToday(){TB_setPlanDate(TB_todayKey())}


function TB_loadBrainStore(){
  try{return JSON.parse(localStorage.getItem(TB_BRAIN_KEY)||"{}")}catch(e){return{}}
}
function TB_saveBrainStore(v){
  localStorage.setItem(TB_BRAIN_KEY,JSON.stringify(v));
}
function TB_renderBrainDump(){
  const el=document.getElementById("tbBrainInput");
  if(!el)return;
  const store=TB_loadBrainStore();
  const item=store[TB_selectedDate]||{text:"",processed:0};
  if(document.activeElement!==el)el.value=item.text||"";
}

function TB_refreshBrainDump(){
  const store=TB_loadBrainStore();
  const old=store[TB_selectedDate]||{};
  const nextGeneration=(Number(old.generation)||1)+1;

  store[TB_selectedDate]={
    text:"",
    processed:0,
    generation:nextGeneration,
    groups:{}
  };

  TB_saveBrainStore(store);

  const input=document.getElementById("tbBrainInput");
  if(input){
    input.value="";
    input.focus();
  }

  // Created tasks remain untouched.
  try{ if(typeof TB_renderStatusDashboard==="function")TB_renderStatusDashboard(); }catch(e){console.error(e);}
}

function TB_brainInputChanged(el){
  const text=el.value;
  const store=TB_loadBrainStore();

  let item=store[TB_selectedDate];
  if(!item || typeof item!=="object"){
    item={text:"",processed:0,generation:1};
  }

  if(!Number.isFinite(Number(item.processed)))item.processed=0;
  if(!Number.isFinite(Number(item.generation)))item.generation=1;

  const parts=text.split(",");
  const completedCount=Math.max(0,parts.length-1);
  const tasks=TB_loadTasks();

  // If user manually removed old text, never keep a processed count
  // larger than the number of comma-finished entries now visible.
  if(item.processed>completedCount){
    item.processed=completedCount;
  }

  // Only create entries that became comma-complete since last input.
  // No title duplicate check — "Delivery, Delivery," must create 2 tasks.
  for(let i=item.processed;i<completedCount;i++){
    const title=String(parts[i]||"").trim();
    if(!title)continue;

    const now=TB_nowIso();

    // Occurrence number for this same task name in the selected date.
    const normalized=title.toLowerCase();
    const existingSame=tasks.filter(function(t){
      return t.planDate===TB_selectedDate &&
             String(t.title||"").trim().toLowerCase()===normalized;
    }).length;

    // Group order: first unique title in this Brain Dump generation = 1,
    // next unique title = 2, etc. Repeats become 1.2, 1.3...
    if(!item.groups || typeof item.groups!=="object")item.groups={};
    if(!item.groups[normalized]){
      const used=Object.keys(item.groups).map(function(k){
        return Number(item.groups[k])||0;
      });
      item.groups[normalized]=(used.length?Math.max.apply(null,used):0)+1;
    }

    const occurrence=existingSame+1;
    const brainOrder=String(item.groups[normalized])+"."+String(occurrence);

    tasks.push({
      id:"tb-"+Date.now()+"-"+i+"-"+Math.random().toString(16).slice(2),
      priority:"",
      title:title,
      type:"Job",
      estimate:20,
      startTime:"",
      manualTime:false,
      autoTime:true,
      planDate:TB_selectedDate,
      status:"Not Started",
      completedDate:"",
      actualMinutes:0,
      source:"brain",
      brainGeneration:item.generation,
      brainOrder:brainOrder,
      createdAt:now,
      startedAt:"",
      holdAt:"",
      doneAt:"",
      statusUpdatedAt:now
    });
  }

  item.text=text;
  item.processed=completedCount;
  store[TB_selectedDate]=item;

  TB_saveBrainStore(store);
  TB_saveTasks(tasks);

  try{
    if(typeof TB_recalculateAutoTimes==="function"){
      TB_recalculateAutoTimes(TB_selectedDate);
    }
  }catch(err){
    console.error("Auto schedule failed:",err);
  }

  // Live counts and open popup.
  try{ if(typeof TB_renderStatusDashboard==="function")TB_renderStatusDashboard(); }catch(e){console.error(e);}
  try{ if(typeof TB_renderTimerTaskOptions==="function")TB_renderTimerTaskOptions(); }catch(e){console.error(e);}
  try{ if(typeof TB_render24HourGrid==="function")TB_render24HourGrid(); }catch(e){console.error(e);}
  try{ if(typeof TB_renderStatusAnalytics==="function")TB_renderStatusAnalytics(); }catch(e){console.error(e);}

  const openStatus=typeof TB_getOpenStatusPopupStatus==="function"
    ? TB_getOpenStatusPopupStatus()
    : "";

  if(openStatus && typeof TB_openStatusDetails==="function"){
    setTimeout(function(){TB_openStatusDetails(openStatus);},0);
  }
}

function TB_deletedTaskSignatures(){
  try{return JSON.parse(localStorage.getItem(TB_DELETED_TASK_KEY)||"{}")}catch(e){return{}}
}
function TB_saveDeletedTaskSignatures(v){
  localStorage.setItem(TB_DELETED_TASK_KEY,JSON.stringify(v));
}
function TB_taskSignature(task){
  return String(task.planDate||"")+"|"+String(task.title||"").trim().toLowerCase();
}
function TB_isPlanningTaskDeleted(task){
  const deleted=TB_deletedTaskSignatures();
  return !!deleted[TB_taskSignature(task)];
}
function TB_markPlanningTaskDeleted(task){
  if(!task)return;
  const deleted=TB_deletedTaskSignatures();
  deleted[TB_taskSignature(task)]=Date.now();
  TB_saveDeletedTaskSignatures(deleted);
}

function TB_addTask(){
  const a=TB_loadTasks();a.push({id:"tb-"+Date.now()+"-"+Math.random().toString(16).slice(2),priority:"",title:"",type:"Job",estimate:20,startTime:"",planDate:TB_selectedDate,status:"Not Started",completedDate:"",actualMinutes:0,source:"manual"});
  TB_saveTasks(a);TB_renderAll();
}
function TB_updateTask(id,f,v){
  const a=TB_loadTasks();
  const t=a.find(function(x){return x.id===id;});
  if(!t)return;

  const oldDate=t.planDate,oldStatus=t.status;

  if(f==="priority"){
    v=String(v||"").replace(/[^\d]/g,"");
    t.priority=v?Math.max(1,Number(v)):"";
  }else if(f==="estimate"){
    t.estimate=Math.max(1,Number(v)||20);
  }else if(f==="startTime"){
    t.startTime=v||"";
    t.manualTime=!!v;
    t.autoTime=!v;
  }else{
    t[f]=v;
  }

  if(f==="status" && oldStatus!==t.status)TB_setStatusTimestamp(t,t.status);
  if(!t.createdAt)t.createdAt=TB_nowIso();

  TB_saveTasks(a);
  if(oldDate)TB_recalculateAutoTimes(oldDate);
  if(t.planDate)TB_recalculateAutoTimes(t.planDate);
  TB_renderAll();
}
function TB_deleteTask(id){
  const popupStatus=TB_getOpenStatusPopupStatus();
  const tasks=TB_loadTasks();
  const task=tasks.find(function(x){return x.id===id;});
  if(!task)return;

  if(task.source==="recurring" && task.recurringId){TB_markRecurringOccurrenceDeleted(task.planDate,task.recurringId);}

  if(typeof TB_markPlanningTaskDeleted==="function"){
    TB_markPlanningTaskDeleted(task);
  }

  TB_saveTasks(tasks.filter(function(x){return x.id!==id;}));

  if(typeof TB_loadSlots==="function" && typeof TB_saveSlots==="function"){
    const slots=TB_loadSlots();
    Object.keys(slots).forEach(function(k){
      if(slots[k] && slots[k].taskId===id){
        delete slots[k];
      }
    });
    TB_saveSlots(slots);
  }

  if(task.planDate && typeof TB_recalculateAutoTimes==="function"){
    TB_recalculateAutoTimes(task.planDate);
  }

  if(typeof TB_renderStatusDashboard==="function")TB_renderStatusDashboard();
  if(typeof TB_renderStatusAnalytics==="function")TB_renderStatusAnalytics();
  if(typeof TB_renderTimerTaskOptions==="function")TB_renderTimerTaskOptions();
  if(typeof TB_render24HourGrid==="function")TB_render24HourGrid();

  // Keep current list open and redraw it immediately.
  if(popupStatus && typeof TB_openStatusDetails==="function"){
    TB_openStatusDetails(popupStatus);
  }
}

let TB_recurringFilter="All";

function TB_loadRecurringBrain(){
  try{return JSON.parse(localStorage.getItem(TB_RECUR_BRAIN_KEY)||'{"text":"","processed":0,"signature":""}')}catch(e){return {text:"",processed:0,signature:""}}
}
function TB_saveRecurringBrain(v){localStorage.setItem(TB_RECUR_BRAIN_KEY,JSON.stringify(v))}

function TB_loadDeletedRecurringOccurrences(){
  try{return JSON.parse(localStorage.getItem(TB_RECUR_DELETED_OCC_KEY)||"{}")}catch(e){return {}}
}
function TB_saveDeletedRecurringOccurrences(v){localStorage.setItem(TB_RECUR_DELETED_OCC_KEY,JSON.stringify(v))}
function TB_recurringOccurrenceKey(dateKey,recurringId){return dateKey+"|"+recurringId}
function TB_markRecurringOccurrenceDeleted(dateKey,recurringId){
  const x=TB_loadDeletedRecurringOccurrences();
  x[TB_recurringOccurrenceKey(dateKey,recurringId)]=Date.now();
  TB_saveDeletedRecurringOccurrences(x);
}
function TB_isRecurringOccurrenceDeleted(dateKey,recurringId){
  return !!TB_loadDeletedRecurringOccurrences()[TB_recurringOccurrenceKey(dateKey,recurringId)];
}

function TB_weekdayName(n){
  return ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"][Number(n)||0];
}
function TB_yearlyMonthDay(dateValue){
  if(!dateValue)return "";
  const p=String(dateValue).split("-");
  return p.length>=3?p[1]+"-"+p[2]:"";
}

function TB_recurringMatchesDate(r,dateKey){
  if(!r || r.active===false)return false;
  const d=TB_dateObj(dateKey);
  const weekday=d.getDay();
  const day=d.getDate();
  const mm=String(d.getMonth()+1).padStart(2,"0");
  const dd=String(day).padStart(2,"0");

  if(r.kind==="Daily")return true;
  if(r.kind==="Weekdays")return weekday>=1 && weekday<=5;
  if(r.kind==="Weekends")return weekday===0 || weekday===6;
  if(r.kind==="Weekly")return Number(r.weekday)===weekday;
  if(r.kind==="Monthly")return Number(r.day)===day;
  if(r.kind==="Yearly"){
    const md=TB_yearlyMonthDay(r.date);
    return md===mm+"-"+dd;
  }
  return false;
}

/*
  A recurring rule creates ONE normal daily task for each matching date.
  That generated task joins the same status dashboard as Brain Dump tasks.
*/
function TB_syncRecurringOccurrencesForDate(dateKey){
  if(!dateKey)return;
  const rules=TB_loadRecurring();
  const tasks=TB_loadTasks();
  let changed=false;

  rules.forEach(function(r){
    if(!TB_recurringMatchesDate(r,dateKey))return;
    if(TB_isRecurringOccurrenceDeleted(dateKey,r.id))return;

    let t=tasks.find(function(x){
      return x.source==="recurring" &&
             x.recurringId===r.id &&
             x.planDate===dateKey;
    });

    if(!t){
      const now=TB_nowIso();
      t={
        id:"tbr-"+dateKey+"-"+r.id+"-"+Math.random().toString(16).slice(2),
        priority:"",
        title:r.title||"Recurring task",
        type:r.type||"Personal",
        estimate:Math.max(1,Number(r.minutes)||20),
        startTime:r.start||"08:00",
        manualTime:true,
        autoTime:false,
        planDate:dateKey,
        status:"Not Started",
        completedDate:"",
        actualMinutes:0,
        source:"recurring",
        recurringId:r.id,
        recurringKind:r.kind,
        createdAt:now,
        startedAt:"",
        holdAt:"",
        doneAt:"",
        statusUpdatedAt:now
      };
      tasks.push(t);
      changed=true;
    }else if(t.status==="Not Started"){
      // Keep an unstarted occurrence aligned with its rule.
      const newTitle=r.title||"Recurring task";
      const newType=r.type||"Personal";
      const newMinutes=Math.max(1,Number(r.minutes)||20);
      const newStart=r.start||"08:00";
      if(t.title!==newTitle || t.type!==newType || Number(t.estimate)!==newMinutes || t.startTime!==newStart){
        t.title=newTitle;t.type=newType;t.estimate=newMinutes;t.startTime=newStart;t.manualTime=true;t.autoTime=false;
        changed=true;
      }
    }
  });

  if(changed)TB_saveTasks(tasks);
}

function TB_syncVisibleRecurringDates(){
  TB_syncRecurringOccurrencesForDate(TB_selectedDate);
  if(TB_selectedDate!==TB_todayKey())TB_syncRecurringOccurrencesForDate(TB_todayKey());
}

function TB_setRecurringFilter(filter,btn){
  TB_recurringFilter=filter;
  document.querySelectorAll(".tb-recurring-filter-row button").forEach(function(b){b.classList.remove("active")});
  if(btn)btn.classList.add("active");
  TB_renderRecurring();
}

function TB_recurringDayFieldHtml(r){
  if(r.kind==="Weekly"){
    return '<select onchange="TB_updateRecurring(\''+r.id+'\',\'weekday\',this.value)">'+
      [0,1,2,3,4,5,6].map(function(n){return '<option value="'+n+'" '+(Number(r.weekday)===n?"selected":"")+'>'+TB_weekdayName(n)+'</option>'}).join("")+
      '</select>';
  }
  if(r.kind==="Monthly"){
    return '<input type="number" min="1" max="31" value="'+esc(r.day||1)+'" onchange="TB_updateRecurring(\''+r.id+'\',\'day\',this.value)">';
  }
  if(r.kind==="Yearly"){
    return '<input type="date" value="'+esc(r.date||"")+'" onchange="TB_updateRecurring(\''+r.id+'\',\'date\',this.value)">';
  }
  if(r.kind==="Weekdays")return '<input value="Mon–Fri" disabled>';
  if(r.kind==="Weekends")return '<input value="Sat–Sun" disabled>';
  return '<input value="Every day" disabled>';
}

function TB_renderRecurringBrainDayField(){
  const kind=(document.getElementById("tbRecurringBrainKind")||{}).value||"Daily";
  const wrap=document.getElementById("tbRecurringBrainDayField");
  if(!wrap)return;

  if(kind==="Weekly"){
    wrap.innerHTML='<select id="tbRecurringBrainDay">'+
      [0,1,2,3,4,5,6].map(function(n){return '<option value="'+n+'" '+(n===1?"selected":"")+'>'+TB_weekdayName(n)+'</option>'}).join("")+
      '</select>';
  }else if(kind==="Monthly"){
    wrap.innerHTML='<input id="tbRecurringBrainDay" type="number" min="1" max="31" value="1">';
  }else if(kind==="Yearly"){
    wrap.innerHTML='<input id="tbRecurringBrainDate" type="date" value="">';
  }else if(kind==="Weekdays"){
    wrap.innerHTML='<input value="Mon–Fri" disabled>';
  }else if(kind==="Weekends"){
    wrap.innerHTML='<input value="Sat–Sun" disabled>';
  }else{
    wrap.innerHTML='<input value="Every day" disabled>';
  }
}

function TB_recurringBrainConfigSignature(){
  const kind=(document.getElementById("tbRecurringBrainKind")||{}).value||"Daily";
  const start=(document.getElementById("tbRecurringBrainStart")||{}).value||"08:00";
  const minutes=Math.max(1,Number((document.getElementById("tbRecurringBrainMinutes")||{}).value)||20);
  const type=(document.getElementById("tbRecurringBrainType")||{}).value||"Personal";
  let extra="";
  if(kind==="Weekly")extra=(document.getElementById("tbRecurringBrainDay")||{}).value||"1";
  if(kind==="Monthly")extra=(document.getElementById("tbRecurringBrainDay")||{}).value||"1";
  if(kind==="Yearly")extra=(document.getElementById("tbRecurringBrainDate")||{}).value||"";
  return [kind,extra,start,minutes,type].join("|");
}

function TB_recurringBrainConfigChanged(resetText=true){
  TB_renderRecurringBrainDayField();
  const state=TB_loadRecurringBrain();
  if(resetText){
    state.text="";
    state.processed=0;
    const input=document.getElementById("tbRecurringBrainInput");
    if(input)input.value="";
  }
  state.signature=TB_recurringBrainConfigSignature();
  TB_saveRecurringBrain(state);
}

function TB_refreshRecurringBrainDump(){
  const state={text:"",processed:0,signature:TB_recurringBrainConfigSignature()};
  TB_saveRecurringBrain(state);
  const input=document.getElementById("tbRecurringBrainInput");
  if(input){input.value="";input.focus();}
}

function TB_recurringBrainInputChanged(el){
  const text=el.value;
  const parts=text.split(",");
  const completed=Math.max(0,parts.length-1);
  const state=TB_loadRecurringBrain();
  const sig=TB_recurringBrainConfigSignature();

  if(state.signature!==sig){
    state.text="";
    state.processed=0;
    state.signature=sig;
  }
  if(state.processed>completed)state.processed=completed;

  const rules=TB_loadRecurring();
  const kind=(document.getElementById("tbRecurringBrainKind")||{}).value||"Daily";
  const start=(document.getElementById("tbRecurringBrainStart")||{}).value||"08:00";
  const minutes=Math.max(1,Number((document.getElementById("tbRecurringBrainMinutes")||{}).value)||20);
  const type=(document.getElementById("tbRecurringBrainType")||{}).value||"Personal";

  let weekday=1,day=1,date="";
  if(kind==="Weekly")weekday=Number((document.getElementById("tbRecurringBrainDay")||{}).value)||1;
  if(kind==="Monthly")day=Math.min(31,Math.max(1,Number((document.getElementById("tbRecurringBrainDay")||{}).value)||1));
  if(kind==="Yearly")date=(document.getElementById("tbRecurringBrainDate")||{}).value||"";

  // Yearly needs a date before commas can create rules.
  if(kind==="Yearly" && !date){
    state.text=text;state.processed=0;TB_saveRecurringBrain(state);
    return;
  }

  for(let i=state.processed;i<completed;i++){
    const title=String(parts[i]||"").trim();
    if(!title)continue;
    rules.push({
      id:"r-"+Date.now()+"-"+i+"-"+Math.random().toString(16).slice(2),
      title:title,
      kind:kind,
      weekday:weekday,
      day:day,
      date:date,
      start:start,
      minutes:minutes,
      type:type,
      active:true
    });
  }

  state.text=text;
  state.processed=completed;
  state.signature=sig;
  TB_saveRecurringBrain(state);
  TB_saveRecurring(rules);

  TB_syncVisibleRecurringDates();
  TB_renderRecurring();
  TB_renderRecurringSummary();
  TB_renderStatusDashboard();
  TB_render24HourGrid();
}

function TB_addRecurring(){
  const a=TB_loadRecurring();
  const id="r-"+Date.now()+"-"+Math.random().toString(16).slice(2);
  a.push({
    id:id,title:"New recurring task",kind:"Daily",weekday:1,day:1,date:"",
    start:"08:00",minutes:20,type:"Personal",active:true
  });
  TB_saveRecurring(a);
  TB_syncVisibleRecurringDates();
  TB_renderRecurring();
  TB_renderRecurringSummary();
  TB_renderStatusDashboard();
  setTimeout(function(){
    const row=document.querySelector('[data-recurring-id="'+id+'"]');
    if(row)row.scrollIntoView({behavior:"smooth",block:"center"});
  },30);
}

function TB_updateRecurring(id,f,v){
  const a=TB_loadRecurring();
  const r=a.find(function(x){return x.id===id;});
  if(!r)return;

  if(f==="day")v=Math.min(31,Math.max(1,Number(v)||1));
  if(f==="weekday")v=Math.min(6,Math.max(0,Number(v)||0));
  if(f==="minutes")v=Math.max(1,Number(v)||20);
  if(f==="active")v=!!v;

  r[f]=v;
  TB_saveRecurring(a);

  TB_syncVisibleRecurringDates();
  TB_renderRecurring();
  TB_renderRecurringSummary();
  TB_renderStatusDashboard();
  TB_render24HourGrid();
}

function TB_deleteRecurring(id){
  TB_saveRecurring(TB_loadRecurring().filter(function(x){return x.id!==id;}));
  TB_renderRecurring();
  TB_renderRecurringSummary();
  TB_renderStatusDashboard();
  TB_render24HourGrid();
}

function TB_renderRecurring(){
  const b=document.getElementById("tbRecurringRows");
  if(!b)return;

  let rows=TB_loadRecurring();
  if(TB_recurringFilter!=="All"){
    rows=rows.filter(function(r){return r.kind===TB_recurringFilter;});
  }

  if(!rows.length){
    b.innerHTML='<div class="tb-empty">No recurring rules in this view.</div>';
    return;
  }

  b.innerHTML=rows.map(function(r){
    return '<div class="tb-recurring-row tb-recurring-row-v96" data-recurring-id="'+esc(r.id)+'">'+
      '<input value="'+esc(r.title||"")+'" onchange="TB_updateRecurring(\''+r.id+'\',\'title\',this.value)" placeholder="Recurring task">'+
      '<select onchange="TB_updateRecurring(\''+r.id+'\',\'kind\',this.value)">'+
        ["Daily","Weekdays","Weekends","Weekly","Monthly","Yearly"].map(function(x){
          return '<option '+(r.kind===x?"selected":"")+'>'+x+'</option>';
        }).join("")+
      '</select>'+
      TB_recurringDayFieldHtml(r)+
      '<input type="time" value="'+esc(r.start||"08:00")+'" onchange="TB_updateRecurring(\''+r.id+'\',\'start\',this.value)">'+
      '<input type="number" min="1" value="'+esc(r.minutes||20)+'" onchange="TB_updateRecurring(\''+r.id+'\',\'minutes\',this.value)">'+
      '<select onchange="TB_updateRecurring(\''+r.id+'\',\'type\',this.value)">'+
        ["Personal","Job","Money","Health","Learning","Other"].map(function(x){
          return '<option '+(r.type===x?"selected":"")+'>'+x+'</option>';
        }).join("")+
      '</select>'+
      '<label class="tb-active-toggle"><input type="checkbox" '+(r.active===false?"":"checked")+' onchange="TB_updateRecurring(\''+r.id+'\',\'active\',this.checked)"></label>'+
      '<button class="tb-delete-task" onclick="TB_deleteRecurring(\''+r.id+'\')">×</button>'+
    '</div>';
  }).join("");
}

function TB_renderRecurringSummary(){
  TB_syncRecurringOccurrencesForDate(TB_selectedDate);
  const scheduled=TB_loadTasks().filter(function(t){
    return t.source==="recurring" && t.planDate===TB_selectedDate;
  });
  const done=scheduled.filter(function(t){return t.status==="Done";}).length;
  const pending=scheduled.length-done;
  const set=function(id,v){const e=document.getElementById(id);if(e)e.textContent=v;};
  set("tbRecurringScheduledCount",scheduled.length);
  set("tbRecurringDoneCount",done);
  set("tbRecurringPendingCount",pending);
}

function TB_openRecurringDetails(filter){
  TB_syncRecurringOccurrencesForDate(TB_selectedDate);
  const modal=document.getElementById("tbRecurringDetailsModal");
  const title=document.getElementById("tbRecurringDetailsTitle");
  const sub=document.getElementById("tbRecurringDetailsSub");
  const body=document.getElementById("tbRecurringDetailsBody");
  if(!modal||!title||!sub||!body)return;

  let rows=TB_loadTasks().filter(function(t){
    return t.source==="recurring" && t.planDate===TB_selectedDate;
  });

  if(filter==="Done")rows=rows.filter(function(t){return t.status==="Done";});
  if(filter==="Not Done")rows=rows.filter(function(t){return t.status!=="Done";});

  title.textContent="🔁 "+(filter==="All"?"Recurring Tasks":filter+" Recurring Tasks");
  sub.textContent=TB_fmtDate(TB_selectedDate)+" · "+rows.length+" item"+(rows.length===1?"":"s");

  if(!rows.length){
    body.innerHTML='<div class="tb-empty">No matching recurring tasks for this date.</div>';
    modal.style.display="flex";return;
  }

  body.innerHTML='<table class="tb-recurring-detail-table"><thead><tr><th>Task</th><th>Repeat</th><th>Type</th><th>Start</th><th>End</th><th>Min</th><th>Status</th></tr></thead><tbody>'+
    rows.map(function(t){
      const end=TB_addMinutesToTime(t.startTime||"08:00",Number(t.estimate)||20);
      return '<tr><td><b>'+esc(t.title)+'</b></td><td>'+esc(t.recurringKind||"")+'</td><td>'+esc(t.type||"Personal")+'</td><td>'+esc(t.startTime||"08:00")+'</td><td>'+esc(end)+'</td><td>'+esc(t.estimate||20)+'</td><td>'+esc(t.status||"Not Started")+'</td></tr>';
    }).join("")+'</tbody></table>';

  modal.style.display="flex";
}

function TB_closeRecurringDetails(){
  const modal=document.getElementById("tbRecurringDetailsModal");
  if(modal)modal.style.display="none";
}

function TB_recurringForDate(k){
  return TB_loadRecurring().filter(function(r){return TB_recurringMatchesDate(r,k);});
}
function TB_slotKey(k,h,m){return k+"|"+String(h).padStart(2,"0")+":"+String(m).padStart(2,"0")}
function TB_minutesFromHHMM(v){const p=String(v||"00:00").split(":");return Number(p[0])*60+Number(p[1])}

function TB_addMinutesToTime(startTime,minutes){
  if(!startTime)return "";
  const p=String(startTime).split(":");
  if(p.length<2)return "";
  const h=Number(p[0]),m=Number(p[1]);
  if(!Number.isFinite(h)||!Number.isFinite(m))return "";
  let total=(h*60+m)+(Number(minutes)||0);
  total=((total%1440)+1440)%1440;
  return String(Math.floor(total/60)).padStart(2,"0")+":"+String(total%60).padStart(2,"0");
}
function TB_nextSlotMinute(n){return Math.ceil(n/20)*20}
function TB_reservedSlotMap(k){
  const map={};

  TB_recurringForDate(k).forEach(function(r){
    const start=TB_minutesFromHHMM(r.start);
    const count=Math.max(1,Math.ceil((Number(r.minutes)||20)/20));
    const status=TB_getRecurringStatus(k,r.id);

    for(let i=0;i<count;i++){
      const minute=(start+i*20)%(24*60);
      const h=Math.floor(minute/60),m=minute%60;

      map[TB_slotKey(k,h,m)]={
        id:r.id,
        title:r.title,
        type:r.type||"Personal",
        minutes:r.minutes||20,
        start:r.start||"08:00",
        status:status,
        source:r.kind==="Daily"?"routine":"recurring"
      };
    }
  });

  return map;
}
function TB_autoSchedulePriorities(){
  const s=TB_loadSlots(),r=TB_reservedSlotMap(TB_selectedDate),a=TB_activeTasksForSelectedDate().filter(t=>Number(t.priority)>0).sort((x,y)=>Number(x.priority)-Number(y.priority));
  Object.keys(s).forEach(k=>{if(k.startsWith(TB_selectedDate+"|")&&s[k]&&s[k].source==="auto")delete s[k]});
  let start=0;if(TB_selectedDate===TB_todayKey()){const n=new Date();start=TB_nextSlotMinute(n.getHours()*60+n.getMinutes())}
  a.forEach(t=>{let need=Math.max(1,Math.ceil((Number(t.estimate)||20)/20));for(let minute=start;minute<1440&&need>0;minute+=20){const h=Math.floor(minute/60),m=minute%60,k=TB_slotKey(TB_selectedDate,h,m);if(!s[k]&&!r[k]){s[k]={taskId:t.id,source:"auto"};need--}}});
  TB_saveSlots(s);TB_render24HourGrid();
}
function TB_clearAutoSlots(){const s=TB_loadSlots();Object.keys(s).forEach(k=>{if(k.startsWith(TB_selectedDate+"|")&&s[k]&&s[k].source==="auto")delete s[k]});TB_saveSlots(s);TB_render24HourGrid()}
function TB_assignSlot(k,id){const s=TB_loadSlots();if(id)s[k]={taskId:id,source:"manual"};else delete s[k];TB_saveSlots(s);TB_render24HourGrid()}


function TB_liveUnscheduledSlotMap(dateKey){
  const map={};
  const reserved=TB_reservedSlotMap(dateKey);

  // Fixed-time tasks also reserve slots first.
  const fixed=TB_plannedTaskSlotMap(dateKey);
  Object.keys(fixed).forEach(function(k){ reserved[k]=true; });

  const manualSlots=TB_loadSlots();
  Object.keys(manualSlots).forEach(function(k){
    if(k.startsWith(dateKey+"|")) reserved[k]=true;
  });

  let startMinute=0;
  if(dateKey===TB_todayKey()){
    const now=new Date();
    startMinute=TB_nextSlotMinute(now.getHours()*60+now.getMinutes());
  }

  // Tasks without a manually selected start time.
  // Priority tasks come first; no-priority tasks follow in the order created.
  const tasks=TB_loadTasks()
    .filter(function(t){
      return t.planDate===dateKey &&
             t.title &&
             !t.startTime &&
             t.status!=="Done" &&
             t.status!=="Moved" &&
             t.status!=="Hold";
    })
    .sort(function(a,b){
      const ap=Number(a.priority)||999999;
      const bp=Number(b.priority)||999999;
      if(ap!==bp)return ap-bp;
      return String(a.id).localeCompare(String(b.id));
    });

  tasks.forEach(function(t){
    let count=Math.max(1,Math.ceil((Number(t.estimate)||20)/20));

    for(let minute=startMinute;minute<1440 && count>0;minute+=20){
      const h=Math.floor(minute/60),m=minute%60;
      const key=TB_slotKey(dateKey,h,m);

      if(!reserved[key] && !map[key]){
        map[key]={
          task:t,
          source:Number(t.priority)>0 ? "priority" : "tentative"
        };
        reserved[key]=true;
        count--;
      }
    }
  });

  return map;
}

function TB_plannedTaskSlotMap(dateKey){
  const map={};

  TB_loadTasks()
    .filter(function(t){
      return t.planDate===dateKey &&
             t.title &&
             t.startTime &&
             t.status!=="Done" &&
             t.status!=="Moved";
    })
    .forEach(function(t){
      const start=TB_minutesFromHHMM(t.startTime);
      const count=Math.max(1,Math.ceil((Number(t.estimate)||20)/20));

      for(let i=0;i<count;i++){
        let minute=start+i*20;
        if(minute>=1440)break;
        const h=Math.floor(minute/60),m=minute%60;
        map[TB_slotKey(dateKey,h,m)]={
          task:t,
          source:"planned"
        };
      }
    });

  return map;
}



function TB_nowIso(){return new Date().toISOString();}
function TB_fmtStamp(v){
  if(!v)return "—";
  const d=new Date(v); if(isNaN(d.getTime()))return "—";
  return d.toLocaleString("en-IN",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit",second:"2-digit"});
}
function TB_minutesToHHMM(total){
  total=((Number(total)||0)%1440+1440)%1440;
  return String(Math.floor(total/60)).padStart(2,"0")+":"+String(total%60).padStart(2,"0");
}
function TB_roundUp20(minute){return Math.ceil(minute/20)*20;}
function TB_defaultAutoStartMinutes(dateKey){
  const now=new Date();
  if(dateKey===TB_todayKey())return TB_roundUp20(now.getHours()*60+now.getMinutes());
  return 6*60;
}
function TB_setStatusTimestamp(t,status){
  const now=TB_nowIso();
  if(!t.createdAt)t.createdAt=now;
  if(status==="Not Started"){t.startedAt="";t.holdAt="";t.doneAt="";t.completedDate="";}
  if(status==="In Progress"){if(!t.startedAt)t.startedAt=now;t.holdAt="";t.doneAt="";t.completedDate="";}
  if(status==="Hold"){t.holdAt=now;t.doneAt="";t.completedDate="";}
  if(status==="Done"){t.doneAt=now;t.completedDate=TB_todayKey();}
  t.statusUpdatedAt=now;
}
function TB_timestampHtml(t){
  return '<b>Task timestamps</b><br>'+
    'Created: '+TB_fmtStamp(t.createdAt)+'<br>'+
    'Started: '+TB_fmtStamp(t.startedAt)+'<br>'+
    'Hold: '+TB_fmtStamp(t.holdAt)+'<br>'+
    'Done: '+TB_fmtStamp(t.doneAt)+'<br>'+
    'Last status change: '+TB_fmtStamp(t.statusUpdatedAt);
}
function TB_recalculateAutoTimes(dateKey){
  const tasks=TB_loadTasks();
  const active=tasks.filter(function(t){
    return t.planDate===dateKey && String(t.title||"").trim() && ["Not Started","In Progress"].includes(t.status);
  }).sort(function(a,b){
    const ap=Number(a.priority)||999999,bp=Number(b.priority)||999999;
    if(ap!==bp)return ap-bp;
    return String(a.createdAt||a.id).localeCompare(String(b.createdAt||b.id));
  });

  let cursor=TB_defaultAutoStartMinutes(dateKey);

  active.forEach(function(t){
    const mins=Math.max(1,Number(t.estimate)||20);
    if(t.manualTime && t.startTime){
      cursor=Math.max(cursor,TB_minutesFromHHMM(t.startTime)+mins);
    }else{
      t.startTime=TB_minutesToHHMM(cursor);
      t.autoTime=true;
      t.manualTime=false;
      cursor+=mins;
    }
  });
  TB_saveTasks(tasks);
}
function TB_upgradeLegacyTasks(){
  const tasks=TB_loadTasks();
  let changed=false;
  tasks.forEach(function(t){
    if(!String(t.title||"").trim())return;
    if(!t.createdAt){t.createdAt=TB_nowIso();changed=true;}
    if(!t.estimate){t.estimate=20;changed=true;}
    if(!["Not Started","In Progress","Done","Hold"].includes(t.status)){t.status="Not Started";changed=true;}
    if(t.manualTime===undefined){t.manualTime=!!t.startTime;changed=true;}
  });
  if(changed)TB_saveTasks(tasks);
  [...new Set(tasks.map(function(t){return t.planDate;}).filter(Boolean))].forEach(TB_recalculateAutoTimes);
}

function TB_openTaskEditor(id){
  const t=TB_loadTasks().find(function(x){return x.id===id;});if(!t)return;
  document.getElementById("tbEditTaskId").value=t.id;
  document.getElementById("tbEditTitle").value=t.title||"";
  document.getElementById("tbEditPriority").value=t.priority||"";
  document.getElementById("tbEditStart").value=t.startTime||"";
  document.getElementById("tbEditDuration").value=t.estimate||20;
  document.getElementById("tbEditDate").value=t.planDate||TB_selectedDate;
  document.getElementById("tbEditType").value=t.type||"Job";
  document.getElementById("tbEditStatus").value=t.status||"Not Started";
  const info=document.getElementById("tbEditTimestampInfo");if(info)info.innerHTML=TB_timestampHtml(t);
  document.getElementById("tbTaskEditorModal").style.display="flex";
}
function TB_closeTaskEditor(){const m=document.getElementById("tbTaskEditorModal");if(m)m.style.display="none";}
function TB_saveTaskEditor(){
  const id=document.getElementById("tbEditTaskId").value,a=TB_loadTasks(),t=a.find(function(x){return x.id===id;});if(!t)return;
  const oldDate=t.planDate,oldStatus=t.status;
  t.title=document.getElementById("tbEditTitle").value.trim();
  const p=String(document.getElementById("tbEditPriority").value||"").replace(/[^\d]/g,"");
  t.priority=p?Math.max(1,Number(p)):"";
  const newStart=document.getElementById("tbEditStart").value||"";
  if(newStart!==t.startTime){t.startTime=newStart;t.manualTime=!!newStart;t.autoTime=!newStart;}
  t.estimate=Math.max(1,Number(document.getElementById("tbEditDuration").value)||20);
  t.planDate=document.getElementById("tbEditDate").value||TB_selectedDate;
  t.type=document.getElementById("tbEditType").value;
  t.status=document.getElementById("tbEditStatus").value;
  if(oldStatus!==t.status)TB_setStatusTimestamp(t,t.status);
  TB_saveTasks(a);
  if(oldDate)TB_recalculateAutoTimes(oldDate);if(t.planDate)TB_recalculateAutoTimes(t.planDate);
  TB_closeTaskEditor();TB_renderAll();
  const smart=document.getElementById("tbSmartPlanPanel");if(smart)smart.classList.add("tb-tool-open");
}
function TB_editorQuickStatus(status){
  const id=document.getElementById("tbEditTaskId").value;TB_closeTaskEditor();TB_quickSetStatus(id,status);
  const p=document.getElementById("tbSmartPlanPanel");if(p)p.classList.add("tb-tool-open");
}
function TB_editorDeleteTask(){
  const id=document.getElementById("tbEditTaskId").value;TB_closeTaskEditor();TB_deleteTask(id);
  const p=document.getElementById("tbSmartPlanPanel");if(p)p.classList.add("tb-tool-open");
}

function TB_rebuildSmartTime(){
  try{TB_syncRecurringOccurrencesForDate(TB_selectedDate)}catch(e){}
  try{if(typeof TB_recalculateAutoTimes==="function")TB_recalculateAutoTimes(TB_selectedDate)}catch(e){}
  TB_render24HourGrid();
}
function TB_render24HourGrid(){
  const b=document.getElementById("tb24HourGrid");
  if(!b)return;

  try{TB_syncRecurringOccurrencesForDate(TB_selectedDate)}catch(e){}
  try{if(typeof TB_recalculateAutoTimes==="function")TB_recalculateAutoTimes(TB_selectedDate)}catch(e){}

  const tasks=TB_loadTasks()
    .filter(function(t){
      return t.planDate===TB_selectedDate &&
             String(t.title||"").trim() &&
             ["Not Started","In Progress","Done","Hold"].includes(t.status);
    })
    .sort(function(a,b){
      return String(a.startTime||"99:99").localeCompare(String(b.startTime||"99:99"));
    });

  if(!tasks.length){
    b.innerHTML='<div class="tb-smart-empty">No tasks are assigned to '+TB_fmtDate(TB_selectedDate)+'. Add tasks in Brain Dump or Recurring.</div>';
    return;
  }

  b.innerHTML='<div class="tb-smart-list">'+tasks.map(function(t){
    const mins=Math.max(1,Number(t.estimate)||20);
    const end=t.startTime?TB_addMinutesToTime(t.startTime,mins):"—";
    const cls=t.status==="In Progress"?" in-progress":t.status==="Done"?" done":t.status==="Hold"?" hold":"";
    const source=t.source==="recurring"?"Recurring · "+(t.recurringKind||""):"Brain / Manual";

    return '<div class="tb-smart-task-row'+cls+'">'+
      '<input type="time" value="'+esc(t.startTime||"")+'" onchange="TB_inlineEditTask(\''+t.id+'\',\'startTime\',this.value)">'+
      '<input value="'+esc(t.title||"")+'" onchange="TB_inlineEditTask(\''+t.id+'\',\'title\',this.value)">'+
      '<input type="number" min="1" value="'+mins+'" onchange="TB_inlineEditTask(\''+t.id+'\',\'estimate\',this.value)">'+
      '<div class="tb-smart-end">'+end+'</div>'+
      '<div><span class="tb-source-pill '+(t.source==="recurring"?"recurring":"")+'">'+esc(source)+'</span></div>'+
      '<select onchange="TB_inlineEditTask(\''+t.id+'\',\'status\',this.value)">'+["Not Started","In Progress","Done","Hold"].map(function(x){return '<option '+(t.status===x?"selected":"")+'>'+x+'</option>'}).join("")+'</select>'+
      '<div class="tb-inline-actions"><button type="button" class="start" onclick="TB_quickSetStatus(\''+t.id+'\',\'In Progress\')">Start</button> <button type="button" class="done" onclick="TB_quickSetStatus(\''+t.id+'\',\'Done\')">Done</button> <button type="button" class="hold" onclick="TB_quickSetStatus(\''+t.id+'\',\'Hold\')">Hold</button></div>'+
    '</div>';
  }).join("")+'</div>';
}
function TB_renderTimerTaskOptions(){const s=document.getElementById("tbTimerTask");if(!s)return;const cur=s.value,a=TB_activeTasksForSelectedDate();s.innerHTML='<option value="">Focus without task</option>'+a.map(t=>'<option value="'+esc(t.id)+'">'+(t.priority?("#"+t.priority+" · "):"")+esc(t.title)+'</option>').join("");if(a.some(t=>t.id===cur))s.value=cur}
function TB_setTimer(n){TB_pauseTimer();TB_timerDefaultSeconds=Math.max(1,Number(n))*60;TB_timerSeconds=TB_timerDefaultSeconds;TB_updateTimerDisplay()}
function TB_setCustomTimer(){const n=Number(document.getElementById("tbCustomMinutes").value);if(n>0)TB_setTimer(n)}
function TB_updateTimerDisplay(){const e=document.getElementById("tbTimerDisplay");if(e)e.textContent=String(Math.floor(TB_timerSeconds/60)).padStart(2,"0")+":"+String(TB_timerSeconds%60).padStart(2,"0")}
function TB_startTimer(){if(TB_timerRunning)return;if(TB_timerSeconds<=0)TB_timerSeconds=TB_timerDefaultSeconds;TB_timerRunning=true;TB_timerInterval=setInterval(()=>{TB_timerSeconds--;TB_updateTimerDisplay();if(TB_timerSeconds<=0)TB_finishTimer()},1000)}
function TB_pauseTimer(){if(TB_timerInterval)clearInterval(TB_timerInterval);TB_timerInterval=null;TB_timerRunning=false}
function TB_resetTimer(){TB_pauseTimer();TB_timerSeconds=TB_timerDefaultSeconds;TB_updateTimerDisplay()}
function TB_addFiveMinutes(){TB_timerSeconds+=300;TB_updateTimerDisplay()}
function TB_finishTimer(){TB_pauseTimer();TB_timerSeconds=0;TB_updateTimerDisplay();const id=(document.getElementById("tbTimerTask")||{}).value||"",mins=Math.max(1,Math.round(TB_timerDefaultSeconds/60));const f=TB_loadFocus();f.push({date:TB_todayKey(),taskId:id,minutes:mins,finishedAt:new Date().toISOString()});TB_saveFocus(f);if(id){const a=TB_loadTasks(),t=a.find(x=>x.id===id);if(t){t.actualMinutes=(Number(t.actualMinutes)||0)+mins;TB_saveTasks(a)}}TB_renderAll();alert("✓ Focus block completed: "+mins+" minutes")}
function TB_renderClock(){
  const now=new Date();
  const clock=document.getElementById("tbCurrentClock");
  const remaining=document.getElementById("tbDayRemaining");

  if(clock){
    clock.textContent=now.toLocaleTimeString("en-IN",{
      hour:"2-digit",
      minute:"2-digit",
      second:"2-digit"
    });
  }

  const midnight=new Date(now);
  midnight.setHours(24,0,0,0);
  const sec=Math.max(0,Math.floor((midnight-now)/1000));
  const hh=Math.floor(sec/3600);
  const mm=Math.floor((sec%3600)/60);

  if(remaining){
    remaining.textContent=String(hh).padStart(2,"0")+"h "+String(mm).padStart(2,"0")+"m";
  }
}
function TB_scrollToNow(){
  if(TB_selectedDate!==TB_todayKey())return;
  const h=new Date().getHours();
  const row=document.getElementById("tbHour-"+h);
  if(row)row.scrollIntoView({behavior:"smooth",block:"center"});
}

function TB_showTimeTool(id,btn){
  const p=document.getElementById(id);
  if(!p)return;
  const alreadyOpen=p.classList.contains("tb-tool-open");

  document.querySelectorAll(".tb-tool-panel").forEach(function(x){x.classList.remove("tb-tool-open");});
  document.querySelectorAll(".tb-command-btn").forEach(function(x){x.classList.remove("active");});

  if(alreadyOpen)return;

  p.classList.add("tb-tool-open");
  if(btn)btn.classList.add("active");

  if(id==="tbRecurringPanel"){TB_renderRecurringBrainDayField();const rs=TB_loadRecurringBrain();const ri=document.getElementById("tbRecurringBrainInput");if(ri)ri.value=rs.text||"";TB_renderRecurring();TB_renderRecurringSummary();}
  if(id==="tbSmartPlanPanel"){TB_render24HourGrid();}
  if(id==="tbBrainPanel"){TB_renderBrainDump();TB_renderTasks();}
  if(id==="tbQuickPanel"){TB_renderClock();TB_renderTimerTaskOptions();}
  if(id==="tbAnalyticsPanel"){TB_renderStatusAnalytics();}

  setTimeout(function(){p.scrollIntoView({behavior:"smooth",block:"start"});},20);
}
function TB_closeTimeTool(id){
  const p=document.getElementById(id);
  if(p)p.classList.remove("tb-tool-open");
  document.querySelectorAll(".tb-command-btn").forEach(function(x){x.classList.remove("active");});
  const bar=document.querySelector(".tb-command-center");
  if(bar)bar.scrollIntoView({behavior:"smooth",block:"start"});
}


function TB_removePopupRowNow(button){
  try{
    const row=button && button.closest ? button.closest("tr") : null;
    if(row){
      row.style.opacity="0";
      row.style.transform="translateX(8px)";
      setTimeout(function(){
        if(row && row.parentNode)row.parentNode.removeChild(row);
      },90);
    }
  }catch(e){}
}

function TB_refreshOpenPopupNow(status){
  if(!status)return;
  // Let localStorage finish first, then redraw from the same canonical source.
  requestAnimationFrame(function(){
    requestAnimationFrame(function(){
      TB_openStatusDetails(status);
    });
  });
}


function TB_safeRender(fnName){
  try{
    const fn=window[fnName];
    if(typeof fn==="function")fn();
  }catch(err){
    console.error(fnName+" failed:",err);
  }
}

function TB_refreshStatusUI(currentPopup){
  // Background counts must update regardless of errors in other panels.
  TB_safeRender("TB_renderStatusDashboard");

  // Other panels are optional and cannot block the popup refresh.
  TB_safeRender("TB_renderTimerTaskOptions");
  TB_safeRender("TB_render24HourGrid");
  TB_safeRender("TB_renderStatusAnalytics");

  if(currentPopup){
    setTimeout(function(){
      try{
        TB_openStatusDetails(currentPopup);
      }catch(err){
        console.error("Popup refresh failed:",err);
      }
    },0);
  }
}

function TB_updatePopupSummaryInstant(task){
  try{
    const summary=document.getElementById("tbStatusDetailsSummary");
    if(!summary)return;

    const cards=summary.querySelectorAll("div");
    if(cards.length>=1){
      const b=cards[0].querySelector("b");
      if(b)b.textContent=Math.max(0,(Number(b.textContent)||0)-1);
    }

    if(cards.length>=2){
      const b=cards[1].querySelector("b");
      if(b){
        const popupStatus=TB_getOpenStatusPopupStatus();
        const remaining=TB_tasksForStatusDashboard(popupStatus)
          .reduce(function(s,t){return s+(Number(t.estimate)||0);},0);
        b.textContent=HL_fmtMinutes(remaining);
      }
    }
  }catch(err){
    console.error("Instant summary update failed:",err);
  }
}

function TB_actionFromPopup(button,id,status){
  const currentPopup=TB_getOpenStatusPopupStatus();
  const tasks=TB_loadTasks();
  const task=tasks.find(function(x){return x.id===id;});
  if(!task)return;

  // Update storage first.
  task.status=status;
  if(typeof TB_setStatusTimestamp==="function"){
    TB_setStatusTimestamp(task,status);
  }
  TB_saveTasks(tasks);

  // Immediate visual change.
  TB_removePopupRowNow(button);
  TB_updatePopupSummaryInstant(task);

  try{
    if(task.planDate && typeof TB_recalculateAutoTimes==="function"){
      TB_recalculateAutoTimes(task.planDate);
    }
  }catch(err){
    console.error("Auto-time recalculation failed:",err);
  }finally{
    // This ALWAYS runs even if Smart Time / Analytics has an error.
    TB_refreshStatusUI(currentPopup);
  }
}

function TB_deleteFromPopup(button,id){
  const currentPopup=TB_getOpenStatusPopupStatus();
  const tasks=TB_loadTasks();
  const task=tasks.find(function(x){return x.id===id;});
  if(!task)return;

  if(task.source==="recurring" && task.recurringId){TB_markRecurringOccurrenceDeleted(task.planDate,task.recurringId);}

  // Remove from storage first.
  TB_saveTasks(tasks.filter(function(x){return x.id!==id;}));

  // Immediate visual change.
  TB_removePopupRowNow(button);
  TB_updatePopupSummaryInstant(task);

  try{
    if(typeof TB_loadSlots==="function" && typeof TB_saveSlots==="function"){
      const slots=TB_loadSlots();
      Object.keys(slots).forEach(function(k){
        if(slots[k] && slots[k].taskId===id)delete slots[k];
      });
      TB_saveSlots(slots);
    }

    if(task.planDate && typeof TB_recalculateAutoTimes==="function"){
      TB_recalculateAutoTimes(task.planDate);
    }
  }catch(err){
    console.error("Delete cleanup failed:",err);
  }finally{
    TB_refreshStatusUI(currentPopup);
  }
}

function TB_getOpenStatusPopupStatus(){
  const modal=document.getElementById("tbStatusDetailsModal");
  if(!modal)return "";

  const visible=
    modal.style.display==="flex" ||
    modal.classList.contains("open") ||
    window.getComputedStyle(modal).display!=="none";

  if(!visible)return "";

  const heading=document.getElementById("tbStatusDetailsTitle");
  if(!heading)return "";

  return heading.textContent
    .replace("📌 ","")
    .replace(" Tasks","")
    .trim();
}

function TB_quickSetStatus(id,status){
  if(!["Not Started","In Progress","Done","Hold"].includes(status))return;

  const popupStatus=TB_getOpenStatusPopupStatus();
  const tasks=TB_loadTasks();
  const task=tasks.find(function(x){return x.id===id;});
  if(!task)return;

  task.status=status;

  if(typeof TB_setStatusTimestamp==="function"){
    TB_setStatusTimestamp(task,status);
  }else{
    const now=new Date().toISOString();
    if(status==="In Progress" && !task.startedAt)task.startedAt=now;
    if(status==="Hold")task.holdAt=now;
    if(status==="Done"){
      task.doneAt=now;
      task.completedDate=TB_todayKey();
    }
    if(status!=="Done")task.completedDate="";
  }

  TB_saveTasks(tasks);

  if(task.planDate && typeof TB_recalculateAutoTimes==="function"){
    TB_recalculateAutoTimes(task.planDate);
  }

  // Update every visible summary immediately.
  if(typeof TB_renderStatusDashboard==="function")TB_renderStatusDashboard();
  if(typeof TB_renderStatusAnalytics==="function")TB_renderStatusAnalytics();
  if(typeof TB_renderTimerTaskOptions==="function")TB_renderTimerTaskOptions();
  if(typeof TB_render24HourGrid==="function")TB_render24HourGrid();

  // IMPORTANT: keep the CURRENT popup open and refresh it.
  // Example: Start from Not Started => row disappears immediately from Not Started.
  if(popupStatus && typeof TB_openStatusDetails==="function"){
    TB_openStatusDetails(popupStatus);
  }
}
function TB_inlineEditTask(id,field,value){
  const currentPopup=TB_getOpenStatusPopupStatus();
  const tasks=TB_loadTasks();
  const task=tasks.find(function(x){return x.id===id;});
  if(!task)return;

  const oldStatus=task.status;
  const oldDate=task.planDate;

  if(field==="priority"){
    const v=String(value||"").replace(/[^\d]/g,"");
    task.priority=v?Math.max(1,Number(v)):"";
  }else if(field==="estimate"){
    task.estimate=Math.max(1,Number(value)||20);
  }else if(field==="startTime"){
    task.startTime=value||"";
    task.manualTime=!!value;
    task.autoTime=!value;
  }else{
    task[field]=value;
  }

  if(field==="status" && oldStatus!==task.status &&
     typeof TB_setStatusTimestamp==="function"){
    TB_setStatusTimestamp(task,task.status);
  }

  TB_saveTasks(tasks);

  try{
    if(oldDate && typeof TB_recalculateAutoTimes==="function"){
      TB_recalculateAutoTimes(oldDate);
    }
    if(task.planDate && task.planDate!==oldDate &&
       typeof TB_recalculateAutoTimes==="function"){
      TB_recalculateAutoTimes(task.planDate);
    }
  }catch(err){
    console.error("Inline edit recalculation failed:",err);
  }finally{
    TB_refreshStatusUI(currentPopup);
  }
}
let TB_statusFilter="";
let TB_analyticsPeriod="Overall";

function TB_filterStatus(status){
  TB_statusFilter=(TB_statusFilter===status)?"":status;
  TB_renderTasks();
}


let TB_statusPeriod="Today";

function TB_dateKeyFromObj(d){
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
}
function TB_periodRange(period){
  const now=TB_dateObj(TB_todayKey());
  let start,end;
  if(period==="Today"){start=new Date(now);end=new Date(now);}
  else if(period==="Week"){
    start=new Date(now);
    const diff=(start.getDay()+6)%7;
    start.setDate(start.getDate()-diff);
    end=new Date(start);end.setDate(end.getDate()+6);
  }else if(period==="Month"){
    start=new Date(now.getFullYear(),now.getMonth(),1);
    end=new Date(now.getFullYear(),now.getMonth()+1,0);
  }else if(period==="Year"){
    start=new Date(now.getFullYear(),0,1);
    end=new Date(now.getFullYear(),11,31);
  }else return null;
  start.setHours(0,0,0,0);end.setHours(23,59,59,999);
  return {start:start,end:end};
}
function TB_inPeriod(dateKey,period){
  if(period==="Overall")return true;
  const r=TB_periodRange(period);if(!r)return true;
  const d=TB_dateObj(dateKey);d.setHours(12,0,0,0);
  return d>=r.start&&d<=r.end;
}
function TB_eachPeriodDate(period,cb){
  const r=TB_periodRange(period);if(!r)return;
  const d=new Date(r.start.getFullYear(),r.start.getMonth(),r.start.getDate());
  const stop=new Date(r.end.getFullYear(),r.end.getMonth(),r.end.getDate());
  while(d<=stop){cb(TB_dateKeyFromObj(d));d.setDate(d.getDate()+1);}
}
function TB_projectRecurringTasks(period){
  if(period==="Today"||period==="Overall")return [];
  const rules=TB_loadRecurring().filter(function(r){return r.active!==false});
  const actual=TB_loadTasks();
  const out=[];
  TB_eachPeriodDate(period,function(dateKey){
    rules.forEach(function(r){
      if(!TB_recurringMatchesDate(r,dateKey))return;
      const exists=actual.some(function(t){
        return t.source==="recurring"&&t.recurringId===r.id&&t.planDate===dateKey;
      });
      if(exists)return;
      out.push({
        id:"proj|"+r.id+"|"+dateKey,
        title:r.title||"Recurring task",
        type:r.type||"Personal",
        estimate:Math.max(1,Number(r.minutes)||20),
        startTime:r.start||"08:00",
        planDate:dateKey,
        status:"Not Started",
        source:"recurring-projection",
        recurringId:r.id,
        recurringKind:r.kind,
        priority:"",
        actualMinutes:0,
        projected:true
      });
    });
  });
  return out;
}
function TB_tasksForPeriod(period){
  const actual=TB_loadTasks().filter(function(t){return String(t.title||"").trim()});
  if(period==="Overall")return actual;
  if(period==="Today"){
    return actual.filter(function(t){
      if(["Not Started","In Progress","Hold"].includes(t.status))return true;
      return t.planDate===TB_todayKey()||t.completedDate===TB_todayKey();
    });
  }
  return actual.filter(function(t){return TB_inPeriod(t.planDate||t.completedDate||TB_todayKey(),period)})
    .concat(TB_projectRecurringTasks(period));
}
function TB_setStatusPeriod(period,btn){
  TB_statusPeriod=period;
  document.querySelectorAll(".tb-status-period-row button").forEach(function(b){b.classList.remove("active")});
  if(btn)btn.classList.add("active");
  const title=document.getElementById("tbStatusPeriodTitle");
  const sub=document.getElementById("tbStatusPeriodSubtitle");
  const label={Today:"Today",Week:"This Week",Month:"This Month",Year:"This Year",Overall:"Overall"}[period];
  if(title)title.textContent="📌 Task Status — "+label;
  if(sub)sub.textContent=(period==="Today")
    ?"See your workload immediately before planning the day."
    :(period==="Overall")
      ?"All stored task history."
      :"Includes actual tasks plus recurring tasks projected for the full selected period.";
  TB_renderStatusDashboard();
}
function TB_tasksForStatusDashboard(status){
  return TB_tasksForPeriod(TB_statusPeriod).filter(function(t){return t.status===status;});
}
function TB_renderStatusDashboard(){
  const map={"Not Started":"tbStatusNotStarted","In Progress":"tbStatusInProgress","Done":"tbStatusDone","Hold":"tbStatusHold"};
  let total=0;
  Object.keys(map).forEach(function(status){
    const n=TB_tasksForStatusDashboard(status).length;
    total+=n;
    const e=document.getElementById(map[status]);if(e)e.textContent=n;
  });
  const t=document.getElementById("tbStatusTotalToday");if(t)t.textContent=total+" task"+(total===1?"":"s");
}
function TB_setAnalyticsPeriod(period,btn){
  TB_analyticsPeriod=period;
  document.querySelectorAll(".tb-analytics-tabs button").forEach(function(b){b.classList.remove("active")});
  if(btn)btn.classList.add("active");
  TB_renderStatusAnalytics();
}

function TB_periodKey(dateStr,period){
  if(!dateStr)return "";
  const d=TB_dateObj(dateStr);

  if(period==="Daily") return dateStr;

  if(period==="Weekly"){
    const temp=new Date(d);
    const day=(temp.getDay()+6)%7;
    temp.setDate(temp.getDate()-day);
    return "Week of "+String(temp.getDate()).padStart(2,"0")+"-"+String(temp.getMonth()+1).padStart(2,"0")+"-"+temp.getFullYear();
  }

  if(period==="Monthly"){
    return d.toLocaleDateString("en-IN",{month:"short",year:"numeric"});
  }

  if(period==="Yearly"){
    return String(d.getFullYear());
  }

  return "Overall";
}

function TB_renderStatusAnalytics(){
  const box=document.getElementById("tbAnalyticsSummary");
  const chart=document.getElementById("tbAnalyticsChart");
  const details=document.getElementById("tbAnalyticsDetails");
  if(!box||!chart||!details)return;

  const tasks=TB_loadTasks().filter(function(t){return String(t.title||"").trim();});
  const statuses=["Not Started","In Progress","Done","Hold"];

  const totals={};
  statuses.forEach(function(s){totals[s]=0});

  tasks.forEach(function(t){
    if(totals[t.status]!==undefined)totals[t.status]++;
  });

  box.innerHTML=statuses.map(function(s){
    return '<div class="tb-analytics-summary-card"><span>'+esc(s)+'</span><b>'+totals[s]+'</b></div>';
  }).join("");

  const grouped={};

  tasks.forEach(function(t){
    const date=t.completedDate||t.planDate||t.createdDate||TB_todayKey();
    const key=TB_periodKey(date,TB_analyticsPeriod);

    if(!grouped[key]){
      grouped[key]={"Not Started":0,"In Progress":0,"Done":0,"Hold":0,total:0};
    }

    if(grouped[key][t.status]!==undefined)grouped[key][t.status]++;
    grouped[key].total++;
  });

  let keys=Object.keys(grouped);

  if(TB_analyticsPeriod==="Overall"){
    keys=["Overall"];
  }

  if(!keys.length){
    chart.innerHTML='<div class="tb-empty">No task history yet.</div>';
    details.innerHTML="";
    return;
  }

  if(TB_analyticsPeriod!=="Overall"){
    keys=keys.slice(-14);
  }

  const max=Math.max(1,...keys.map(function(k){
    return Math.max(...statuses.map(function(s){return grouped[k][s]||0}));
  }));

  const W=Math.max(760,keys.length*90);
  const H=220,L=35,R=15,T=15,B=40,cw=W-L-R,ch=H-T-B;
  const step=cw/keys.length;
  const groupWidth=Math.min(58,step*.72);
  const barW=Math.max(5,(groupWidth-8)/statuses.length);
  const colors=["#94a3b8","#facc15","#22c55e","#ef4444"];

  let svg='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="none" style="min-width:'+W+'px">';

  for(let i=0;i<=4;i++){
    const y=T+ch*i/4;
    svg+='<line x1="'+L+'" y1="'+y+'" x2="'+(W-R)+'" y2="'+y+'" stroke="#e8edf3"/>';
  }

  keys.forEach(function(k,ki){
    const center=L+step*ki+step/2;
    const start=center-groupWidth/2;

    statuses.forEach(function(s,si){
      const v=grouped[k][s]||0;
      const h=ch*(v/max);
      const x=start+si*(barW+2);
      const y=T+ch-h;
      svg+='<rect x="'+x+'" y="'+y+'" width="'+barW+'" height="'+h+'" rx="2" fill="'+colors[si]+'"/>';
    });

    svg+='<text x="'+center+'" y="'+(H-14)+'" text-anchor="middle" font-size="9" fill="#64748b">'+esc(k)+'</text>';
  });

  svg+='</svg>';
  chart.innerHTML='<div style="overflow-x:auto">'+svg+'</div>';

  details.innerHTML=
    '<table><thead><tr><th>Period</th>'+
    statuses.map(function(s){return '<th>'+esc(s)+'</th>'}).join("")+
    '<th>Total</th></tr></thead><tbody>'+
    keys.map(function(k){
      return '<tr><td>'+esc(k)+'</td>'+
        statuses.map(function(s){return '<td>'+(grouped[k][s]||0)+'</td>'}).join("")+
        '<td><b>'+grouped[k].total+'</b></td></tr>';
    }).join("")+
    '</tbody></table>';
}

function TB_renderAll(){
  if(typeof TB_seedTasksIfNeeded==="function")TB_seedTasksIfNeeded();
  if(typeof TB_upgradeLegacyTasks==="function")TB_upgradeLegacyTasks();
  if(typeof TB_seedRecurringIfNeeded==="function")TB_seedRecurringIfNeeded();
  TB_syncVisibleRecurringDates();

  if(typeof TB_renderStatusDashboard==="function")TB_renderStatusDashboard();
  if(typeof TB_renderStatusAnalytics==="function")TB_renderStatusAnalytics();

  const d=document.getElementById("tbPlanDate");
  if(d)d.value=TB_selectedDate;

  if(typeof TB_renderClock==="function")TB_renderClock();
  if(typeof TB_renderBrainDump==="function")TB_renderBrainDump();
  if(typeof TB_renderRecurring==="function")TB_renderRecurring();
  if(typeof TB_renderRecurringSummary==="function")TB_renderRecurringSummary();
  if(typeof TB_renderTimerTaskOptions==="function")TB_renderTimerTaskOptions();
  if(typeof TB_render24HourGrid==="function")TB_render24HourGrid();
  if(typeof TB_updateTimerDisplay==="function")TB_updateTimerDisplay();
}
setInterval(TB_renderClock,1000);


/* ============================================================
   V74 HEALTH TRACKER
   ============================================================ */
const HL_FOOD_KEY="healthFoodsV1";
const HL_WEIGHT_KEY="healthWeightsV1";
const HL_SLEEP_KEY="healthSleepV1";
let HL_selectedDate=HL_todayKey();
let HL_mealFilter="All";

/*
 Common-food reference calories.
 These are approximate defaults per listed unit, intended for personal tracking.
 Users can override calories manually per row.
*/
const HL_FOOD_DB={
  "Idli":{unit:"piece",cal:60},
  "Dosa":{unit:"piece",cal:170},
  "Chapati":{unit:"piece",cal:110},
  "White Rice":{unit:"cup",cal:205},
  "Brown Rice":{unit:"cup",cal:215},
  "Dal":{unit:"cup",cal:180},
  "Sambar":{unit:"cup",cal:120},
  "Curd":{unit:"cup",cal:150},
  "Upma":{unit:"cup",cal:220},
  "Pongal":{unit:"cup",cal:280},
  "Poori":{unit:"piece",cal:100},
  "Vada":{unit:"piece",cal:150},
  "Egg":{unit:"piece",cal:78},
  "Boiled Egg":{unit:"piece",cal:78},
  "Chicken":{unit:"100 g",cal:165},
  "Fish":{unit:"100 g",cal:140},
  "Milk":{unit:"cup",cal:120},
  "Tea":{unit:"cup",cal:80},
  "Coffee":{unit:"cup",cal:90},
  "Banana":{unit:"piece",cal:105},
  "Apple":{unit:"piece",cal:95},
  "Orange":{unit:"piece",cal:62},
  "Biscuits":{unit:"piece",cal:45},
  "Bread":{unit:"slice",cal:80},
  "Peanut":{unit:"30 g",cal:170},
  "Almonds":{unit:"10 pieces",cal:70},
  "Potato":{unit:"100 g",cal:87},
  "Vegetable Curry":{unit:"cup",cal:180},
  "Paneer":{unit:"100 g",cal:265},
  "Noodles":{unit:"plate",cal:350},
  "Biryani":{unit:"plate",cal:500}
};

function HL_todayKey(){
  const d=new Date();
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
}
function HL_dateObj(k){return new Date(k+"T00:00:00")}
function HL_load(key){try{return JSON.parse(localStorage.getItem(key)||"[]")}catch(e){return[]}}
function HL_save(key,v){localStorage.setItem(key,JSON.stringify(v))}
function HL_setDate(v){if(!v)return;HL_selectedDate=v;HL_renderAll()}
function HL_changeDate(n){
  const d=HL_dateObj(HL_selectedDate);d.setDate(d.getDate()+n);
  HL_setDate(d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0"));
}
function HL_goToday(){HL_setDate(HL_todayKey())}

function HL_foods(){return HL_load(HL_FOOD_KEY)}
function HL_weights(){return HL_load(HL_WEIGHT_KEY)}
function HL_sleeps(){return HL_load(HL_SLEEP_KEY)}

function HL_addFoodRow(){
  const a=HL_foods();
  a.push({
    id:"hf-"+Date.now()+"-"+Math.random().toString(16).slice(2),
    date:HL_selectedDate,meal:"Breakfast",food:"",qty:1,unit:"piece",calories:0,manual:false
  });
  HL_save(HL_FOOD_KEY,a);HL_renderFood();
}
function HL_updateFood(id,field,value){
  const a=HL_foods(),r=a.find(x=>x.id===id);if(!r)return;
  if(field==="qty")value=Math.max(0,Number(value)||0);
  if(field==="calories"){value=Math.max(0,Number(value)||0);r.manual=true}
  r[field]=value;
  if(field==="food"){
    const db=HL_FOOD_DB[value];
    if(db){r.unit=db.unit;r.manual=false;r.calories=(Number(r.qty)||1)*db.cal}
  }
  if(field==="qty"&&!r.manual){
    const db=HL_FOOD_DB[r.food];
    if(db)r.calories=(Number(r.qty)||0)*db.cal;
  }
  HL_save(HL_FOOD_KEY,a);HL_renderFood();HL_renderSummary();
}
function HL_deleteFood(id){HL_save(HL_FOOD_KEY,HL_foods().filter(x=>x.id!==id));HL_renderFood();HL_renderSummary()}
function HL_setMealFilter(v,btn){
  HL_mealFilter=v;
  document.querySelectorAll("#hlMealTabs button").forEach(b=>b.classList.remove("active"));
  if(btn)btn.classList.add("active");
  HL_renderFood();
}
function HL_foodOptions(current){
  const names=Object.keys(HL_FOOD_DB);
  let h='<option value="">Choose / type below</option>';
  names.forEach(n=>h+='<option value="'+esc(n)+'" '+(current===n?"selected":"")+'>'+esc(n)+'</option>');
  return h;
}
function HL_renderFood(){
  const box=document.getElementById("hlFoodRows");if(!box)return;
  let a=HL_foods().filter(x=>x.date===HL_selectedDate);
  if(HL_mealFilter!=="All")a=a.filter(x=>x.meal===HL_mealFilter);

  if(!a.length){
    box.innerHTML='<div class="health-empty">No food entered for this selection. Click + Add Food.</div>';
  }else{
    box.innerHTML=a.map(r=>
      '<div class="health-food-row">'+
        '<select onchange="HL_updateFood(\''+r.id+'\',\'meal\',this.value)">'+
          ["Breakfast","Lunch","Dinner","Snack"].map(x=>'<option '+(r.meal===x?"selected":"")+'>'+x+'</option>').join("")+
        '</select>'+
        '<div>'+
          '<select onchange="HL_updateFood(\''+r.id+'\',\'food\',this.value)">'+HL_foodOptions(r.food)+'</select>'+
          (r.food&&!(r.food in HL_FOOD_DB)?'<input value="'+esc(r.food)+'" onchange="HL_updateFood(\''+r.id+'\',\'food\',this.value)" style="margin-top:4px">':'')+
        '</div>'+
        '<input type="number" min="0" step="0.5" value="'+esc(r.qty||0)+'" onchange="HL_updateFood(\''+r.id+'\',\'qty\',this.value)">'+
        '<input value="'+esc(r.unit||"")+'" onchange="HL_updateFood(\''+r.id+'\',\'unit\',this.value)">'+
        '<input type="number" min="0" value="'+esc(Math.round(r.calories||0))+'" onchange="HL_updateFood(\''+r.id+'\',\'calories\',this.value)" title="You can override automatic calories">'+
        '<button class="health-remove-btn" onclick="HL_deleteFood(\''+r.id+'\')">×</button>'+
      '</div>'
    ).join("");
  }
  const total=HL_foods().filter(x=>x.date===HL_selectedDate).reduce((s,x)=>s+(Number(x.calories)||0),0);
  const t=document.getElementById("hlFoodTotalBottom");if(t)t.textContent=Math.round(total).toLocaleString("en-IN")+" kcal";
}

function HL_saveWeight(){
  const d=(document.getElementById("hlWeightDate")||{}).value||HL_selectedDate;
  const v=Number((document.getElementById("hlWeightValue")||{}).value);
  if(!v||v<=0){alert("Enter a valid weight.");return}
  let a=HL_weights().filter(x=>x.date!==d);
  a.push({date:d,weight:v});a.sort((x,y)=>x.date.localeCompare(y.date));HL_save(HL_WEIGHT_KEY,a);
  document.getElementById("hlWeightValue").value="";
  HL_renderWeight();HL_renderSummary();
}

function HL_minutesBetween(start,end){
  const p1=String(start).split(":"),p2=String(end).split(":");
  let a=Number(p1[0])*60+Number(p1[1]),b=Number(p2[0])*60+Number(p2[1]);
  if(b<=a)b+=1440;
  return Math.max(0,b-a);
}
function HL_fmtMinutes(m){return Math.floor(m/60)+"h "+String(m%60).padStart(2,"0")+"m"}
function HL_updateSleepPreview(){
  const s=(document.getElementById("hlSleepStart")||{}).value||"23:00";
  const e=(document.getElementById("hlSleepEnd")||{}).value||"06:00";
  const x=document.getElementById("hlSleepPreview");if(x)x.textContent=HL_fmtMinutes(HL_minutesBetween(s,e));
}
function HL_saveSleep(){
  const d=(document.getElementById("hlSleepDate")||{}).value||HL_selectedDate;
  const s=(document.getElementById("hlSleepStart")||{}).value;
  const e=(document.getElementById("hlSleepEnd")||{}).value;
  if(!s||!e){alert("Enter sleep and wake time.");return}
  let a=HL_sleeps().filter(x=>x.date!==d);
  a.push({date:d,start:s,end:e,minutes:HL_minutesBetween(s,e)});a.sort((x,y)=>x.date.localeCompare(y.date));HL_save(HL_SLEEP_KEY,a);
  HL_renderSleep();HL_renderSummary();
}

function HL_lastNDays(records,n,dateField){
  const end=HL_dateObj(HL_selectedDate),start=new Date(end);start.setDate(start.getDate()-(n-1));
  return records.filter(r=>{const d=HL_dateObj(r[dateField]);return d>=start&&d<=end});
}
function HL_renderLineChart(boxId,rows,valueKey,suffix){
  const box=document.getElementById(boxId);if(!box)return;
  const data=rows.slice(-30);
  if(!data.length){box.innerHTML='<div class="health-empty">No history yet.</div>';return}
  const vals=data.map(x=>Number(x[valueKey])||0),min=Math.min(...vals),max=Math.max(...vals),range=Math.max(1,max-min);
  const W=650,H=180,L=35,R=15,T=15,B=30,cw=W-L-R,ch=H-T-B;
  let svg='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="none">';
  for(let i=0;i<=3;i++){const y=T+ch*i/3;svg+='<line x1="'+L+'" y1="'+y+'" x2="'+(W-R)+'" y2="'+y+'" stroke="#e8edf3"/>'}
  let pts=[];
  data.forEach((r,i)=>{
    const x=L+(data.length===1?cw/2:cw*i/(data.length-1));
    const y=T+ch-( (Number(r[valueKey])-min)/range*ch );
    pts.push(x+","+y);
  });
  svg+='<polyline fill="none" stroke="#2563eb" stroke-width="3" points="'+pts.join(" ")+'"/>';
  data.forEach((r,i)=>{
    const x=L+(data.length===1?cw/2:cw*i/(data.length-1));
    const y=T+ch-( (Number(r[valueKey])-min)/range*ch );
    svg+='<circle cx="'+x+'" cy="'+y+'" r="3.5" fill="#2563eb"/>';
    if(i===data.length-1)svg+='<text x="'+(x-4)+'" y="'+Math.max(12,y-8)+'" text-anchor="end" font-size="9" font-weight="700" fill="#1d4ed8">'+(Number(r[valueKey]).toFixed(valueKey==="weight"?1:0))+suffix+'</text>';
  });
  svg+='</svg>';box.innerHTML=svg;
}
function HL_renderWeight(){
  const a=HL_weights().slice().sort((x,y)=>x.date.localeCompare(y.date));
  const latest=a[a.length-1];
  const latestEl=document.getElementById("hlWeightLatest2");if(latestEl)latestEl.textContent=latest?latest.weight.toFixed(1)+" kg":"—";
  function changeForDays(n){
    if(!latest)return null;
    const cutoff=new Date(HL_dateObj(latest.date));cutoff.setDate(cutoff.getDate()-n);
    const prev=a.filter(x=>HL_dateObj(x.date)<=cutoff).pop();
    return prev?latest.weight-prev.weight:null;
  }
  const c7=changeForDays(7),c30=changeForDays(30);
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
  set("hlWeight7Change",c7===null?"—":((c7>0?"+":"")+c7.toFixed(1)+" kg"));
  set("hlWeight30Change",c30===null?"—":((c30>0?"+":"")+c30.toFixed(1)+" kg"));
  HL_renderLineChart("hlWeightChart",a,"weight"," kg");
  const h=document.getElementById("hlWeightHistory");if(h)h.innerHTML=a.length?'<table><thead><tr><th>Date</th><th>Weight</th></tr></thead><tbody>'+
    a.slice().reverse().slice(0,12).map(x=>'<tr><td>'+esc(x.date)+'</td><td>'+x.weight.toFixed(1)+' kg</td></tr>').join("")+'</tbody></table>':'';
}
function HL_renderSleep(){
  const a=HL_sleeps().slice().sort((x,y)=>x.date.localeCompare(y.date));
  const selected=a.find(x=>x.date===HL_selectedDate),last=a[a.length-1];
  const lastEl=document.getElementById("hlSleepLast");if(lastEl)lastEl.textContent=selected?HL_fmtMinutes(selected.minutes):(last?HL_fmtMinutes(last.minutes):"—");
  const avg=n=>{const r=HL_lastNDays(a,n,"date");return r.length?Math.round(r.reduce((s,x)=>s+x.minutes,0)/r.length):null};
  const a7=avg(7),a30=avg(30),set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
  set("hlSleep7Avg",a7===null?"—":HL_fmtMinutes(a7));set("hlSleep30Avg",a30===null?"—":HL_fmtMinutes(a30));
  HL_renderLineChart("hlSleepChart",a.map(x=>({date:x.date,hours:x.minutes/60})),"hours"," h");
  const h=document.getElementById("hlSleepHistory");if(h)h.innerHTML=a.length?'<table><thead><tr><th>Date</th><th>Sleep</th></tr></thead><tbody>'+
    a.slice().reverse().slice(0,12).map(x=>'<tr><td>'+esc(x.date)+'</td><td>'+HL_fmtMinutes(x.minutes)+'</td></tr>').join("")+'</tbody></table>':'';
}

function HL_renderSummary(){
  const foods=HL_foods().filter(x=>x.date===HL_selectedDate),cal=foods.reduce((s,x)=>s+(Number(x.calories)||0),0);
  const c=document.getElementById("hlCaloriesToday");if(c)c.textContent=Math.round(cal).toLocaleString("en-IN")+" kcal";
  const mc=document.getElementById("hlMealCount");if(mc)mc.textContent=foods.length+" food entr"+(foods.length===1?"y":"ies");
  const w=HL_weights().slice().sort((a,b)=>a.date.localeCompare(b.date)),latest=w[w.length-1],prev=w[w.length-2];
  const lw=document.getElementById("hlLatestWeight");if(lw)lw.textContent=latest?latest.weight.toFixed(1)+" kg":"— kg";
  const wc=document.getElementById("hlWeightChange");if(wc)wc.textContent=latest&&prev?("Previous: "+prev.weight.toFixed(1)+" kg"):"No previous reading";
  const s=HL_sleeps().find(x=>x.date===HL_selectedDate),sl=document.getElementById("hlSleepToday");if(sl)sl.textContent=s?(s.minutes/60).toFixed(1)+" h":"— h";
  const week=HL_lastNDays(HL_sleeps(),7,"date"),av=week.length?Math.round(week.reduce((z,x)=>z+x.minutes,0)/week.length):null;
  const sa=document.getElementById("hlSleepAverage");if(sa)sa.textContent="7-day average: "+(av===null?"—":HL_fmtMinutes(av));
}
function HL_renderAll(){
  const d=document.getElementById("hlDate");if(d)d.value=HL_selectedDate;
  const wd=document.getElementById("hlWeightDate");if(wd)wd.value=HL_selectedDate;
  const sd=document.getElementById("hlSleepDate");if(sd)sd.value=HL_selectedDate;
  HL_renderFood();HL_renderWeight();HL_renderSleep();HL_renderSummary();HL_updateSleepPreview();
}
setTimeout(function(){
  const s=document.getElementById("hlSleepStart"),e=document.getElementById("hlSleepEnd");
  if(s)s.addEventListener("input",HL_updateSleepPreview);
  if(e)e.addEventListener("input",HL_updateSleepPreview);
},0);


/* V83 LEARNING TRACKER */
const LR_SKILLS="lrSkillsV1",LR_TOPICS="lrTopicsV1",LR_PROJECTS="lrProjectsV1",LR_NOTES="lrNotesV1",LR_GOALS="lrGoalsV1";
let LR_skill="python",LR_filter="All";
function LR_today(){const d=new Date();return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function LR_get(k,f){try{const v=localStorage.getItem(k);return v?JSON.parse(v):f}catch(e){return f}}
function LR_set(k,v){localStorage.setItem(k,JSON.stringify(v))}
function LR_mins(n){n=Math.round(Number(n)||0);return n>=60?Math.floor(n/60)+"h "+n%60+"m":n+"m"}
function LR_defaultTopics(){return [
["1. Basics","Install Python & First Program","Python, editor, print(), comments"],["1. Basics","Variables & Data Types","int, float, str, bool"],["1. Basics","Strings","indexing, slicing, formatting, methods"],["1. Basics","Numbers & Operators","arithmetic, comparison, logical operators"],["1. Basics","User Input","input() and type conversion"],
["2. Conditions & Loops","if / elif / else","decision making"],["2. Conditions & Loops","for Loops","range(), iteration and nested loops"],["2. Conditions & Loops","while Loops","break, continue and loop conditions"],
["3. Data Structures","Lists","append, remove, sort, slicing"],["3. Data Structures","Tuples","immutable sequences and unpacking"],["3. Data Structures","Sets","unique values and set operations"],["3. Data Structures","Dictionaries","key-value data and loops"],
["4. Functions","Functions","def, parameters and return"],["4. Functions","Scope & Reusable Code","local/global scope"],["4. Functions","Useful Built-ins","lambda, enumerate, zip, map/filter"],
["5. Files & Errors","Read & Write Files","text files and paths"],["5. Files & Errors","CSV Files","read and write CSV"],["5. Files & Errors","Error Handling","try, except and debugging"],
["6. Modules","Modules & Imports","built-in and custom modules"],["6. Modules","pip & Virtual Environments","packages and isolated environments"],
["7. OOP","Classes & Objects","class, __init__, methods"],["7. OOP","Inheritance","reuse and extend classes"],
["8. Data Analysis","NumPy Basics","arrays and calculations"],["8. Data Analysis","pandas Basics","DataFrames, CSV and Excel"],["8. Data Analysis","pandas Data Cleaning","grouping, merging and missing data"],["8. Data Analysis","Matplotlib","basic charts"],
["9. Automation","File & Folder Automation","rename, move and organize files"],["9. Automation","Excel Automation","openpyxl / pandas reports"],["9. Automation","Automated Test Report","process test results and summarize"],
["10. APIs & JSON","JSON","read and transform JSON"],["10. APIs & JSON","REST APIs","requests and responses"],
["11. Projects","Expense / CSV Analyzer","analyze transactions"],["11. Projects","Automated Test Report Project","turn test data into a report"],["11. Projects","Personal Automation Project","automate one repeated task"]
].map((x,i)=>({id:"py"+(i+1),stage:x[0],title:x[1],detail:x[2],status:"Not Started",review:""}))}
function LR_seed(){
 let s=LR_get(LR_SKILLS,[]);if(!s.length){s=[{id:"python",name:"Python",icon:"🐍",desc:"Programming, automation, data analysis and practical projects."}];LR_set(LR_SKILLS,s)}
 let t=LR_get(LR_TOPICS,{});if(!t.python){t.python=LR_defaultTopics();LR_set(LR_TOPICS,t)}
 let p=LR_get(LR_PROJECTS,{});if(!p.python){p.python=[{id:"p1",title:"Python Mini Exercises",status:"Not Started"},{id:"p2",title:"Expense / CSV Analyzer",status:"Not Started"},{id:"p3",title:"Automated Test Report",status:"Not Started"}];LR_set(LR_PROJECTS,p)}
}
function LR_topics(){return (LR_get(LR_TOPICS,{})[LR_skill]||[])}
function LR_projects(){return (LR_get(LR_PROJECTS,{})[LR_skill]||[])}
function LR_progress(id){const a=(LR_get(LR_TOPICS,{})[id]||[]);return a.length?Math.round(a.filter(x=>x.status==="Completed").length/a.length*100):0}
function LR_skillTime(skill){
 let mins=0;
 if(typeof TB_loadFocus==="function"&&typeof TB_loadTasks==="function"){
   const logs=TB_loadFocus(),tasks=TB_loadTasks();
   logs.forEach(f=>{const t=tasks.find(x=>x.id===f.taskId);if(t&&(String(t.type).toLowerCase()==="learning"||String(t.title||"").toLowerCase().includes(String(skill.name||"").toLowerCase())))mins+=Number(f.minutes)||0})
 }
 return mins;
}
function LR_renderSkills(){
 const b=document.getElementById("lrSkillCards");if(!b)return;const s=LR_get(LR_SKILLS,[]);
 b.innerHTML=s.map(x=>'<button class="lr-skill-card '+(x.id===LR_skill?"active":"")+'" onclick="LR_select(\''+x.id+'\')"><div class="ico">'+x.icon+'</div><h3>'+esc(x.name)+'</h3><p>'+esc(x.desc||"")+'</p><div class="lr-mini"><span style="width:'+LR_progress(x.id)+'%"></span></div><p style="margin-top:4px">'+LR_progress(x.id)+'% complete</p></button>').join("")
}
function LR_select(id){LR_skill=id;LR_render()}
function LR_addSkill(){const n=prompt("Skill name:");if(!n)return;const id="skill"+Date.now(),s=LR_get(LR_SKILLS,[]);s.push({id,name:n,icon:"📘",desc:"New skill"});LR_set(LR_SKILLS,s);let t=LR_get(LR_TOPICS,{});t[id]=[];LR_set(LR_TOPICS,t);LR_skill=id;LR_render()}
function LR_updateTopic(id,f,v){let all=LR_get(LR_TOPICS,{}),t=(all[LR_skill]||[]).find(x=>x.id===id);if(!t)return;t[f]=v;if(f==="status"&&v==="Completed"&&!t.review){let d=new Date();d.setDate(d.getDate()+7);t.review=d.toISOString().slice(0,10)}LR_set(LR_TOPICS,all);LR_render()}
function LR_setFilter(v,btn){LR_filter=v;document.querySelectorAll(".lr-filters button").forEach(x=>x.classList.remove("active"));if(btn)btn.classList.add("active");LR_renderRoadmap()}
function LR_renderRoadmap(){
 const b=document.getElementById("lrRoadmap");if(!b)return;let a=LR_topics();if(LR_filter!=="All")a=a.filter(x=>x.status===LR_filter);if(!a.length){b.innerHTML='<div class="tb-empty">No topics in this filter.</div>';return}
 const g={};a.forEach(x=>(g[x.stage]||(g[x.stage]=[])).push(x));
 b.innerHTML=Object.keys(g).map(k=>'<div class="lr-stage"><div class="lr-stage-head"><b>'+esc(k)+'</b><span>'+g[k].filter(x=>x.status==="Completed").length+' / '+g[k].length+' completed</span></div>'+g[k].map(t=>'<div class="lr-topic"><div><b>'+esc(t.title)+'</b><small>'+esc(t.detail)+'</small></div><select onchange="LR_updateTopic(\''+t.id+'\',\'status\',this.value)">'+["Not Started","Learning","Practicing","Completed"].map(s=>'<option '+(t.status===s?"selected":"")+'>'+s+'</option>').join("")+'</select><input type="date" value="'+esc(t.review||"")+'" onchange="LR_updateTopic(\''+t.id+'\',\'review\',this.value)"></div>').join("")+'</div>').join("")
}
function LR_addProject(){const n=prompt("Project name:");if(!n)return;let all=LR_get(LR_PROJECTS,{});(all[LR_skill]||(all[LR_skill]=[])).push({id:"p"+Date.now(),title:n,status:"Not Started"});LR_set(LR_PROJECTS,all);LR_renderProjects()}
function LR_updateProject(id,f,v){let all=LR_get(LR_PROJECTS,{}),p=(all[LR_skill]||[]).find(x=>x.id===id);if(!p)return;p[f]=v;LR_set(LR_PROJECTS,all);LR_render()}
function LR_deleteProject(id){let all=LR_get(LR_PROJECTS,{});all[LR_skill]=(all[LR_skill]||[]).filter(x=>x.id!==id);LR_set(LR_PROJECTS,all);LR_renderProjects()}
function LR_renderProjects(){const b=document.getElementById("lrProjects");if(!b)return;const a=LR_projects();b.innerHTML=a.length?a.map(p=>'<div class="lr-project"><input value="'+esc(p.title)+'" onchange="LR_updateProject(\''+p.id+'\',\'title\',this.value)"><select onchange="LR_updateProject(\''+p.id+'\',\'status\',this.value)">'+["Not Started","In Progress","Done"].map(s=>'<option '+(p.status===s?"selected":"")+'>'+s+'</option>').join("")+'</select><button class="tb-delete-task" onclick="LR_deleteProject(\''+p.id+'\')">×</button></div>').join(""):'<div class="tb-empty">No projects yet.</div>'}
function LR_saveGoal(v){let g=LR_get(LR_GOALS,{});g[LR_skill]=Math.max(5,Number(v)||30);LR_set(LR_GOALS,g);LR_renderGoal()}
function LR_todayMinutes(skill){
 let mins=0;if(typeof TB_loadFocus==="function"&&typeof TB_loadTasks==="function"){const logs=TB_loadFocus(),tasks=TB_loadTasks();logs.filter(f=>f.date===LR_today()).forEach(f=>{const t=tasks.find(x=>x.id===f.taskId);if(t&&(String(t.type).toLowerCase()==="learning"||String(t.title||"").toLowerCase().includes(skill.name.toLowerCase())))mins+=Number(f.minutes)||0})}return mins
}
function LR_renderGoal(){const skill=LR_get(LR_SKILLS,[]).find(x=>x.id===LR_skill);if(!skill)return;const g=LR_get(LR_GOALS,{})[LR_skill]||30,mins=LR_todayMinutes(skill),pct=Math.min(100,Math.round(mins/g*100));document.getElementById("lrDailyGoal").value=g;document.getElementById("lrTodayProgress").innerHTML='<div class="lr-goal-bar"><span style="width:'+pct+'%"></span></div><div class="lr-goal-cap"><span>'+mins+' min completed</span><b>'+pct+'%</b></div>'}
function LR_scheduleLearning(){
 const skill=LR_get(LR_SKILLS,[]).find(x=>x.id===LR_skill);if(!skill)return;const next=LR_topics().find(x=>x.status!=="Completed"),min=Number(document.getElementById("lrDailyGoal").value)||30;
 if(typeof TB_loadTasks==="function"&&typeof TB_saveTasks==="function"){const a=TB_loadTasks();a.push({id:"tb-learn-"+Date.now(),priority:"",title:skill.name+" Learning"+(next?" — "+next.title:""),type:"Learning",estimate:min,startTime:"",planDate:LR_today(),status:"Not Started",completedDate:"",actualMinutes:0,source:"learning"});TB_saveTasks(a)}
 alert("Added "+min+" minutes of "+skill.name+" to today's Time planner.")
}
function LR_saveNote(v){let n=LR_get(LR_NOTES,{});n[LR_skill+"|"+LR_today()]=v;LR_set(LR_NOTES,n)}
function LR_clearNote(){let n=LR_get(LR_NOTES,{});delete n[LR_skill+"|"+LR_today()];LR_set(LR_NOTES,n);document.getElementById("lrTodayNote").value=""}
function LR_renderReviews(){const b=document.getElementById("lrReviews");if(!b)return;const d=LR_today(),a=LR_topics().filter(x=>x.status==="Completed"&&x.review&&x.review<=d);b.innerHTML=a.length?a.map(x=>'<div class="lr-review"><b>'+esc(x.title)+'</b><span>Review due '+esc(x.review)+' · solve one small exercise.</span></div>').join(""):'<div class="tb-empty">Nothing due for review.</div>'}
function LR_renderHistory(){const b=document.getElementById("lrHistory");if(!b)return;const n=LR_get(LR_NOTES,{}),rows=Object.keys(n).filter(k=>k.startsWith(LR_skill+"|")&&String(n[k]).trim()).map(k=>({date:k.split("|")[1],note:n[k]})).sort((a,b)=>b.date.localeCompare(a.date));b.innerHTML=rows.length?'<table><thead><tr><th>Date</th><th>Notes</th></tr></thead><tbody>'+rows.map(r=>'<tr><td>'+r.date+'</td><td>'+esc(r.note)+'</td></tr>').join("")+'</tbody></table>':'<div class="tb-empty">No learning notes yet.</div>'}
function LR_streak(){
 const n=LR_get(LR_NOTES,{}),days={};Object.keys(n).filter(k=>k.startsWith(LR_skill+"|")&&String(n[k]).trim()).forEach(k=>days[k.split("|")[1]]=1);
 if(typeof TB_loadFocus==="function"&&typeof TB_loadTasks==="function"){const logs=TB_loadFocus(),tasks=TB_loadTasks(),skill=LR_get(LR_SKILLS,[]).find(x=>x.id===LR_skill);logs.forEach(f=>{const t=tasks.find(x=>x.id===f.taskId);if(t&&skill&&(String(t.type).toLowerCase()==="learning"||String(t.title||"").toLowerCase().includes(skill.name.toLowerCase())))days[f.date]=1})}
 let d=new Date(),s=0;while(true){const k=d.toISOString().slice(0,10);if(days[k]){s++;d.setDate(d.getDate()-1)}else break}return s
}
function LR_render(){
 LR_seed();const skills=LR_get(LR_SKILLS,[]),skill=skills.find(x=>x.id===LR_skill)||skills[0];if(!skill)return;LR_skill=skill.id;const t=LR_topics(),done=t.filter(x=>x.status==="Completed").length,p=t.length?Math.round(done/t.length*100):0,prac=t.filter(x=>x.status==="Practicing").length,rev=t.filter(x=>x.status==="Completed"&&x.review&&x.review<=LR_today()).length,time=LR_skillTime(skill);
 document.getElementById("lrActiveSkills").textContent=skills.length;document.getElementById("lrTopicsDone").textContent=skills.reduce((s,x)=>s+(LR_get(LR_TOPICS,{})[x.id]||[]).filter(y=>y.status==="Completed").length,0);document.getElementById("lrTotalTime").textContent=LR_mins(skills.reduce((s,x)=>s+LR_skillTime(x),0));document.getElementById("lrStreak").textContent=LR_streak()+" days";
 document.getElementById("lrSkillName").textContent=skill.name;document.getElementById("lrSkillDesc").textContent=skill.desc||"";document.getElementById("lrProgressPct").textContent=p+"%";document.getElementById("lrProgressCircle").style.background="conic-gradient(#2563eb "+(p*3.6)+"deg,#e2e8f0 0deg)";document.getElementById("lrCompleted").textContent=done+" / "+t.length;document.getElementById("lrSkillTime").textContent=LR_mins(time);document.getElementById("lrPracticing").textContent=prac;document.getElementById("lrReviewDue").textContent=rev;
 const next=t.find(x=>x.status!=="Completed");document.getElementById("lrContinue").innerHTML=next?'<h3>'+esc(next.title)+'</h3><p>'+esc(next.detail)+'</p><button class="primary" onclick="LR_updateTopic(\''+next.id+'\',\'status\',\'Learning\')">Start Topic</button>':'<div class="tb-empty">Roadmap complete 🎉</div>';
 const notes=LR_get(LR_NOTES,{});document.getElementById("lrTodayNote").value=notes[LR_skill+"|"+LR_today()]||"";document.getElementById("lrNoteDate").textContent=LR_today();
 LR_renderSkills();LR_renderGoal();LR_renderRoadmap();LR_renderProjects();LR_renderReviews();LR_renderHistory()
}

/* V84 FULL PAGE LEARNING NOTES */
const LR_FULL_NOTES_KEY="lrFullNotesV1";
let LR_currentNoteId="",LR_noteAutosaveTimer=null;

function LR_cloudAvailable(){
  return typeof google!=="undefined" &&
         google.script &&
         google.script.run;
}
function LR_setCloudState(text,kind){
  const e=document.getElementById("lrNotesCloudState");
  if(!e)return;
  e.textContent=text;
  e.classList.remove("ok","wait","err");
  if(kind)e.classList.add(kind);
}
function LR_notePayload(note){
  const skills=LR_get(LR_SKILLS,[]);
  const sk=skills.find(function(s){return s.id===note.skillId;});
  return {
    id:note.id||"",
    title:note.title||"Untitled Note",
    skillId:note.skillId||"",
    skillName:sk?sk.name:"",
    date:note.date||LR_today(),
    body:note.body||"",
    created:note.created||new Date().toISOString(),
    updated:note.updated||new Date().toISOString()
  };
}
function LR_saveNoteToSheet(note){
  if(!LR_cloudAvailable()){
    LR_setCloudState("☁ Sheet unavailable","err");
    return;
  }

  LR_setCloudState("☁ Saving...","wait");

  google.script.run
    .withSuccessHandler(function(res){
      if(res && res.success){
        LR_setCloudState("☁ Sheet saved","ok");
      }else{
        LR_setCloudState("☁ Save failed","err");
      }
    })
    .withFailureHandler(function(){
      LR_setCloudState("☁ Save failed","err");
    })
    .LRGS_saveLearningNote(LR_notePayload(note));
}
function LR_syncNotesFromSheet(){
  if(!LR_cloudAvailable()){
    LR_setCloudState("☁ Sheet unavailable","err");
    return;
  }

  LR_setCloudState("☁ Syncing...","wait");

  google.script.run
    .withSuccessHandler(function(res){
      if(!res || !res.success || !Array.isArray(res.notes)){
        LR_setCloudState("☁ Sync failed","err");
        return;
      }

      const local=LR_loadFullNotes();
      const map={};

      local.forEach(function(n){ if(n && n.id)map[n.id]=n; });

      res.notes.forEach(function(n){
        if(!n || !n.id)return;
        const old=map[n.id];
        if(!old || String(n.updated||"") >= String(old.updated||"")){
          map[n.id]=n;
        }
      });

      const merged=Object.keys(map).map(function(k){return map[k];});
      LR_saveFullNotes(merged);
      LR_renderNotesList();

      if(LR_currentNoteId && map[LR_currentNoteId]){
        LR_loadNoteIntoEditor(LR_currentNoteId);
      }else if(merged.length){
        LR_loadNoteIntoEditor(
          merged.slice().sort(function(a,b){
            return String(b.updated||"").localeCompare(String(a.updated||""));
          })[0].id
        );
      }

      LR_setCloudState("☁ Sheet synced","ok");
    })
    .withFailureHandler(function(){
      LR_setCloudState("☁ Sync failed","err");
    })
    .LRGS_getLearningNotes();
}
function LR_loadFullNotes(){return LR_get(LR_FULL_NOTES_KEY,[])}
function LR_saveFullNotes(v){LR_set(LR_FULL_NOTES_KEY,v)}
function LR_openNotesPage(){
 const p=document.getElementById("lrNotesPage");if(!p)return;p.classList.add("open");LR_populateNoteSkillSelect();
 const a=LR_loadFullNotes();if(a.length)LR_loadNoteIntoEditor(a.slice().sort((x,y)=>String(y.updated).localeCompare(String(x.updated)))[0].id);else LR_newNote();LR_renderNotesList();setTimeout(LR_syncNotesFromSheet,100)
}
function LR_closeNotesPage(){LR_saveCurrentNote(false);document.getElementById("lrNotesPage").classList.remove("open")}
function LR_populateNoteSkillSelect(){const s=document.getElementById("lrFullNoteSkill");if(!s)return;const a=LR_get(LR_SKILLS,[]),cur=s.value||LR_skill;s.innerHTML=a.map(x=>'<option value="'+esc(x.id)+'">'+esc(x.name)+'</option>').join("");if(a.some(x=>x.id===cur))s.value=cur}
function LR_newNote(){
 LR_saveCurrentNote(false);const n={id:"note-"+Date.now()+"-"+Math.random().toString(16).slice(2),title:"New Note",skillId:LR_skill||"python",date:LR_today(),body:"",created:new Date().toISOString(),updated:new Date().toISOString()};
 const a=LR_loadFullNotes();a.push(n);LR_saveFullNotes(a);LR_currentNoteId=n.id;LR_loadNoteIntoEditor(n.id);LR_renderNotesList();LR_saveNoteToSheet(n);setTimeout(()=>{const t=document.getElementById("lrFullNoteTitle");if(t){t.focus();t.select()}},30)
}
function LR_loadNoteIntoEditor(id){
 const n=LR_loadFullNotes().find(x=>x.id===id);if(!n)return;LR_currentNoteId=id;LR_populateNoteSkillSelect();
 document.getElementById("lrFullNoteTitle").value=n.title||"";document.getElementById("lrFullNoteSkill").value=n.skillId||LR_skill;document.getElementById("lrFullNoteDate").value=n.date||LR_today();document.getElementById("lrFullNoteBody").value=n.body||"";
 const st=document.getElementById("lrNotesSaveState");st.textContent="Saved";st.classList.remove("unsaved");document.getElementById("lrNotesLastSaved").textContent=n.updated?"Last saved: "+new Date(n.updated).toLocaleString("en-IN"):"Not saved yet";LR_updateNoteWordCount();LR_renderNotesList()
}
function LR_noteEditorChanged(){const st=document.getElementById("lrNotesSaveState");st.textContent="Unsaved";st.classList.add("unsaved");LR_updateNoteWordCount();clearTimeout(LR_noteAutosaveTimer);LR_noteAutosaveTimer=setTimeout(()=>LR_saveCurrentNote(false),1200)}
function LR_saveCurrentNote(show){
 if(!LR_currentNoteId)return;const a=LR_loadFullNotes(),n=a.find(x=>x.id===LR_currentNoteId);if(!n)return;
 n.title=(document.getElementById("lrFullNoteTitle").value||"Untitled Note").trim()||"Untitled Note";n.skillId=document.getElementById("lrFullNoteSkill").value||LR_skill;n.date=document.getElementById("lrFullNoteDate").value||LR_today();n.body=document.getElementById("lrFullNoteBody").value||"";n.updated=new Date().toISOString();LR_saveFullNotes(a);LR_saveNoteToSheet(n);
 const st=document.getElementById("lrNotesSaveState");st.textContent=show?"✓ Saved":"Saved";st.classList.remove("unsaved");document.getElementById("lrNotesLastSaved").textContent="Last saved: "+new Date(n.updated).toLocaleString("en-IN");LR_renderNotesList();if(show)setTimeout(()=>st.textContent="Saved",900)
}
function LR_renderNotesList(){
 const b=document.getElementById("lrNotesList");if(!b)return;const q=String(document.getElementById("lrNotesSearch").value||"").toLowerCase().trim();let a=LR_loadFullNotes().slice().sort((x,y)=>String(y.updated).localeCompare(String(x.updated)));if(q)a=a.filter(n=>String(n.title||"").toLowerCase().includes(q)||String(n.body||"").toLowerCase().includes(q));
 document.getElementById("lrNotesCount").textContent=a.length+" note"+(a.length===1?"":"s");const skills=LR_get(LR_SKILLS,[]);
 b.innerHTML=a.length?a.map(n=>{const sk=skills.find(s=>s.id===n.skillId),prev=String(n.body||"").replace(/\s+/g," ").slice(0,75);return '<button class="lr-note-list-item '+(n.id===LR_currentNoteId?"active":"")+'" onclick="LR_saveCurrentNote(false);LR_loadNoteIntoEditor(\''+n.id+'\')"><b>'+esc(n.title||"Untitled Note")+'</b><span>'+esc(sk?sk.name:"Learning")+' · '+esc(n.date||"")+'</span><small>'+esc(prev||"Empty note")+'</small></button>'}).join(""):'<div class="tb-empty">No notes found.</div>'
}
function LR_insertNoteText(t){const e=document.getElementById("lrFullNoteBody");if(!e)return;const s=e.selectionStart||0,en=e.selectionEnd||0,v=e.value||"";e.value=v.slice(0,s)+t+v.slice(en);e.selectionStart=e.selectionEnd=s+t.length;e.focus();LR_noteEditorChanged()}
function LR_updateNoteWordCount(){const v=document.getElementById("lrFullNoteBody").value||"",w=v.trim()?v.trim().split(/\s+/).length:0;document.getElementById("lrNotesWordCount").textContent=w+" word"+(w===1?"":"s")}
function LR_exportNotesBackup(){
 LR_saveCurrentNote(false);const payload={app:"My Tracking Learning Notes",version:1,exportedAt:new Date().toISOString(),notes:LR_loadFullNotes()},blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="My_Tracking_Learning_Notes_Backup_"+LR_today()+".json";document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),500)
}
function LR_importNotesBackup(file){
 if(!file)return;const r=new FileReader();r.onload=function(){try{const d=JSON.parse(r.result),inc=Array.isArray(d)?d:d.notes;if(!Array.isArray(inc))throw new Error();const map={};LR_loadFullNotes().forEach(n=>map[n.id]=n);inc.forEach(n=>{if(n&&n.id)map[n.id]=n});LR_saveFullNotes(Object.values(map));LR_renderNotesList();alert("Notes backup restored successfully.")}catch(e){alert("Could not restore this backup file.")}document.getElementById("lrNotesImportInput").value=""};r.readAsText(file)
}

/* ============================================================
   V106 STOCK PERFORMANCE SCANNER
   ============================================================ */
var ST_data={headers:[],stocks:[]};
var ST_period="1D";
var ST_customDays=4;
var ST_filterMode="all";
var ST_loaded=false;

function ST_num(v){
  const n=Number(v);
  return Number.isFinite(n)?n:0;
}
function ST_money(v){
  const n=ST_num(v);
  return "₹"+n.toLocaleString("en-IN",{minimumFractionDigits:2,maximumFractionDigits:2});
}
function ST_pct(v){
  const n=ST_num(v);
  return (n>=0?"+":"")+n.toFixed(2)+"%";
}
function ST_dateObj(iso){
  const p=String(iso||"").split("-");
  if(p.length!==3)return null;
  return new Date(Number(p[0]),Number(p[1])-1,Number(p[2]));
}
function ST_diffDays(aIso,bIso){
  const a=ST_dateObj(aIso),b=ST_dateObj(bIso);
  if(!a||!b)return 0;
  return Math.round((a-b)/(24*60*60*1000));
}
function ST_periodLabel(){
  if(ST_period==="1D")return "1 Day";
  if(ST_period==="1W")return "1 Week";
  if(ST_period==="6M")return "6 Months";
  if(ST_period==="1Y")return "1 Year";
  return ST_customDays+" Days";
}
function ST_setPeriod(period,btn){
  ST_period=period;
  document.querySelectorAll("[data-st-period]").forEach(function(b){b.classList.remove("active")});
  if(btn)btn.classList.add("active");

  const custom=document.getElementById("stCustomControls");
  if(custom)custom.classList.toggle("visible",period==="CUSTOM");

  ST_render();
}
function ST_setCustomDays(days,btn){
  ST_customDays=Math.max(1,Number(days)||2);
  document.querySelectorAll("[data-st-custom]").forEach(function(b){b.classList.remove("active")});
  if(btn)btn.classList.add("active");
  ST_period="CUSTOM";

  document.querySelectorAll("[data-st-period]").forEach(function(b){
    b.classList.toggle("active",b.dataset.stPeriod==="CUSTOM");
  });

  const custom=document.getElementById("stCustomControls");
  if(custom)custom.classList.add("visible");

  ST_render();
}
function ST_toggleOnlyGainers(){
  ST_filterMode="gainers";
  ST_render();
}
function ST_toggleOnlyLosers(){
  ST_filterMode="losers";
  ST_render();
}
function ST_resetFilters(){
  ST_filterMode="all";
  const q=document.getElementById("stSearch");
  if(q)q.value="";
  ST_render();
}

/*
  Select the start price.

  1D and Custom use price observations/trading sessions:
    1D = latest vs previous valid price
    Custom 2 = latest vs 2 valid observations back
    Custom 8 = latest vs 8 valid observations back

  1W / 6M / 1Y use calendar targets:
    choose the closest valid price at or before the target date.
*/
function ST_pickStart(prices){
  if(!Array.isArray(prices)||prices.length<2)return null;

  const latest=prices[0];

  if(ST_period==="1D"){
    return prices.length>1?prices[1]:null;
  }

  if(ST_period==="CUSTOM"){
    const idx=ST_customDays;
    return prices.length>idx?prices[idx]:null;
  }

  const latestDate=ST_dateObj(latest.date);
  if(!latestDate)return null;

  const target=new Date(latestDate);

  if(ST_period==="1W"){
    target.setDate(target.getDate()-7);
  }else if(ST_period==="6M"){
    target.setMonth(target.getMonth()-6);
  }else if(ST_period==="1Y"){
    target.setFullYear(target.getFullYear()-1);
  }

  const targetIso=
    target.getFullYear()+"-"+
    String(target.getMonth()+1).padStart(2,"0")+"-"+
    String(target.getDate()).padStart(2,"0");

  // prices are newest -> oldest.
  for(let i=1;i<prices.length;i++){
    if(prices[i].date<=targetIso)return prices[i];
  }

  return null;
}
function ST_periodPrices(prices,start,latest){
  if(!start||!latest)return [];
  return prices.filter(function(p){
    return p.date<=latest.date && p.date>=start.date;
  });
}
function ST_buildRows(){
  const q=String((document.getElementById("stSearch")||{}).value||"").trim().toLowerCase();
  const requireFull=String((document.getElementById("stMinHistory")||{}).value||"0")==="1";
  const sectorFilter=String((document.getElementById("stSectorFilter")||{}).value||"ALL");
  const capFilter=String((document.getElementById("stCapFilter")||{}).value||"ALL");
  const rows=[];
  (ST_data.stocks||[]).forEach(function(s){
    const sector=s.sector||"Other / Review",capital=s.capital||"Unclassified";
    const hay=[s.symbol,s.ticker,s.company,sector,capital].join(" ").toLowerCase();
    if(q&&!hay.includes(q))return;if(sectorFilter!=="ALL"&&sector!==sectorFilter)return;if(capFilter!=="ALL"&&capital!==capFilter)return;
    const prices=(s.prices||[]).filter(p=>ST_num(p.price)>0);if(!prices.length)return;
    const latest=prices[0],start=ST_pickStart(prices);
    if(!start){if(requireFull)return;rows.push({symbol:s.symbol,ticker:s.ticker,company:s.company,sector,capital,insufficient:true,latest});return;}
    const startPrice=ST_num(start.price),latestPrice=ST_num(latest.price);if(startPrice<=0||latestPrice<=0)return;
    const value100=(latestPrice/startPrice)*100,returnPct=value100-100,periodPrices=ST_periodPrices(prices,start,latest);
    const avg=periodPrices.length?periodPrices.reduce((sum,p)=>sum+ST_num(p.price),0)/periodPrices.length:0;
    let upDays=0,downDays=0,flatDays=0;for(let i=periodPrices.length-1;i>0;i--){const older=ST_num(periodPrices[i].price),newer=ST_num(periodPrices[i-1].price);if(newer>older)upDays++;else if(newer<older)downDays++;else flatDays++;}
    const comparedDays=Math.max(0,periodPrices.length-1);
    if(ST_filterMode==="gainers"&&returnPct<=0)return;if(ST_filterMode==="losers"&&returnPct>=0)return;
    rows.push({symbol:s.symbol,ticker:s.ticker,company:s.company,sector,capital,start,latest,startPrice,latestPrice,averagePrice:avg,returnPct,value100,observationCount:periodPrices.length,upDays,downDays,flatDays,comparedDays,insufficient:false});
  });
  rows.sort(function(a,b){if(a.insufficient&&!b.insufficient)return 1;if(!a.insufficient&&b.insufficient)return -1;if(a.insufficient&&b.insufficient)return String(a.symbol).localeCompare(String(b.symbol));return b.value100-a.value100;});return rows;
}
function ST_render(){
  const body=document.getElementById("stTableBody");if(!body)return;
  if(!ST_loaded){body.innerHTML='<tr><td colspan="11" class="st-empty">Loading stocks sheet…</td></tr>';return;}
  const rows=ST_buildRows(),valid=rows.filter(r=>!r.insufficient);
  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
  set("stSummaryPeriod",ST_periodLabel());set("stPeriodTitle",ST_periodLabel()+" Performance");set("stSummaryCount",valid.length);
  const best=valid.length?valid[0]:null,worst=valid.length?valid[valid.length-1]:null;
  set("stSummaryBest",best?ST_money(best.value100):"—");set("stSummaryBestStock",best?(best.symbol+" · "+ST_pct(best.returnPct)):"—");set("stSummaryWorst",worst?ST_money(worst.value100):"—");set("stSummaryWorstStock",worst?(worst.symbol+" · "+ST_pct(worst.returnPct)):"—");
  if(best){const sd=best.start.displayDate||best.start.date,ld=best.latest.displayDate||best.latest.date;set("stSummaryDates",sd+" → "+ld);set("stGlobalStartDate",sd);set("stGlobalLatestDate",ld);}else{set("stSummaryDates","Insufficient history");set("stGlobalStartDate","—");set("stGlobalLatestDate","—");}
  if(!rows.length){body.innerHTML='<tr><td colspan="11" class="st-empty">No stocks match this filter.</td></tr>';return;}
  let rank=0;body.innerHTML=rows.map(function(r){
    if(r.insufficient)return '<tr><td>—</td><td><div class="st-symbol">'+esc(r.symbol||"")+'</div><div class="st-ticker">'+esc(r.ticker||"")+'</div></td><td>'+esc(r.company||"")+'</td><td><span class="st-sector-pill">'+esc(r.sector||"")+'</span></td><td><span class="st-cap-pill">'+esc(r.capital||"")+'</span></td><td colspan="6" class="st-insufficient">Not enough price history for '+esc(ST_periodLabel())+'.</td></tr>';
    rank++;const cls=r.returnPct>0?"st-positive":r.returnPct<0?"st-negative":"st-neutral",valueCls=r.value100>100?"up":r.value100<100?"down":"";let tc="st-trend-flat",arrow="→";if(r.upDays>r.downDays){tc="st-trend-up";arrow="↑"}else if(r.downDays>r.upDays){tc="st-trend-down";arrow="↓"}const trend=r.comparedDays?(r.upDays+"/"+r.comparedDays+" "+arrow):"—";
    return '<tr><td class="st-rank">'+rank+'</td><td><div class="st-symbol">'+esc(r.symbol||"")+'</div><div class="st-ticker">'+esc(r.ticker||"")+'</div></td><td title="'+esc(r.company||"")+'">'+esc(r.company||"")+'</td><td title="'+esc(r.sector||"")+'"><span class="st-sector-pill">'+esc(r.sector||"")+'</span></td><td><span class="st-cap-pill">'+esc(r.capital||"")+'</span></td><td>'+ST_money(r.startPrice)+'</td><td>'+ST_money(r.latestPrice)+'</td><td>'+ST_money(r.averagePrice)+'</td><td class="'+cls+'">'+ST_pct(r.returnPct)+'</td><td><span class="st-value '+valueCls+'">'+ST_money(r.value100)+'</span></td><td class="'+tc+'">'+trend+'</td></tr>';
  }).join("");
}
function ST_applyData(result){
  if(!result||!result.success)throw new Error((result&&result.message)||"Could not read stocks sheet.");
  ST_data={headers:Array.isArray(result.headers)?result.headers:[],stocks:Array.isArray(result.stocks)?result.stocks:[]};ST_loaded=true;
  const status=document.getElementById("stSyncStatus");if(status){status.textContent="✓ "+ST_data.stocks.length+" stocks loaded · "+ST_data.headers.length+" dated price columns";status.style.color="#15803d";}
  const range=document.getElementById("stDateRange");if(range)range.textContent=ST_data.headers.length?((ST_data.headers[0].displayDate||ST_data.headers[0].date)+" → "+(ST_data.headers[ST_data.headers.length-1].displayDate||ST_data.headers[ST_data.headers.length-1].date)):"No dated columns found";
  const ss=document.getElementById("stSectorFilter");if(ss){const cur=ss.value||"ALL",vals=[...new Set(ST_data.stocks.map(s=>String(s.sector||"Other / Review").trim()).filter(Boolean))].sort((a,b)=>a.localeCompare(b));ss.innerHTML='<option value="ALL">All Sectors</option>'+vals.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join("");if(vals.includes(cur))ss.value=cur;}
  const cs=document.getElementById("stCapFilter");if(cs){const cur=cs.value||"ALL",pref=["Large Cap","Mid Cap","Small Cap"],vals=[...new Set(ST_data.stocks.map(s=>String(s.capital||"Unclassified").trim()).filter(Boolean))];vals.sort((a,b)=>{const ai=pref.indexOf(a),bi=pref.indexOf(b);if(ai!=-1&&bi!=-1)return ai-bi;if(ai!=-1)return -1;if(bi!=-1)return 1;return a.localeCompare(b)});cs.innerHTML='<option value="ALL">All Market Caps</option>'+vals.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join("");if(vals.includes(cur))cs.value=cur;}
  ST_render();
}
function ST_sync(showMessage,forceRefresh){
  const status=document.getElementById("stSyncStatus");
  const body=document.getElementById("stTableBody");

  if(status){
    status.textContent=forceRefresh?"Refreshing stocks data…":"Loading stocks data…";
    status.style.color="#64748b";
  }
  if(body && !ST_loaded){
    body.innerHTML='<tr><td colspan="11" class="st-empty">Loading stocks…</td></tr>';
  }

  if(typeof google==="undefined" || !google.script || !google.script.run){
    if(status){status.textContent="Google Apps Script connection unavailable.";status.style.color="#dc2626";}
    return;
  }

  const success=function(result){
    try{
      ST_applyData(result);
      if(status){
        const extra=result&&result.cached?" · cached":"";
        status.textContent="✓ "+ST_data.stocks.length+" stocks · "+
          ((result&&result.loadedPriceColumns)||ST_data.headers.length)+" price dates"+extra;
        status.style.color="#15803d";
      }
      if(showMessage)alert("Stocks loaded successfully.\n"+ST_data.stocks.length+" stocks.");
    }catch(err){
      if(status){status.textContent="Stock load failed: "+err.message;status.style.color="#dc2626";}
      if(body){body.innerHTML='<tr><td colspan="11" class="st-empty">Could not load stocks: '+esc(err.message)+'</td></tr>';}
      if(showMessage)alert("Stock load failed.\n"+err.message);
    }
  };

  const failure=function(err){
    const msg=(err&&err.message)?err.message:String(err);
    if(status){status.textContent="Stock load failed: "+msg;status.style.color="#dc2626";}
    if(body){body.innerHTML='<tr><td colspan="11" class="st-empty">Could not load stocks: '+esc(msg)+'</td></tr>';}
    if(showMessage)alert("Stock load failed.\n"+msg);
  };

  if(forceRefresh){
    google.script.run
      .withSuccessHandler(success)
      .withFailureHandler(failure)
      .refreshStocksForWeb();
  }else{
    google.script.run
      .withSuccessHandler(success)
      .withFailureHandler(failure)
      .getStocksForWeb();
  }
}

function ST_showTool(which,btn){
  document.querySelectorAll(".stock-tool-panel").forEach(function(p){p.classList.remove("open")});
  document.querySelectorAll(".stock-tool-card").forEach(function(b){b.classList.remove("active")});

  if(btn)btn.classList.add("active");

  if(which==="scanner"){
    const p=document.getElementById("stScannerTool");
    if(p)p.classList.add("open");

    if(!ST_loaded){
      ST_sync(false,false);
    }else{
      ST_render();
    }
  }else if(which==="pro"){
    const p=document.getElementById("stProTool");
    if(p)p.classList.add("open");

    // V111 Pro Analyzer is internet-powered and independent from stocks sheet.
    STP_init();
  }else{
    const p=document.getElementById("stPreviousTool");
    if(p)p.classList.add("open");
  }
}
function ST_closeTools(){
  document.querySelectorAll(".stock-tool-panel").forEach(function(p){p.classList.remove("open")});
  document.querySelectorAll(".stock-tool-card").forEach(function(b){b.classList.remove("active")});
}


/* ============================================================
   V111 INTERNET PRO STOCK ANALYZER
   ============================================================ */
var STP_marketData=null;
var STP_searchTimer=null;

function STP_init(){
  const input=document.getElementById("stpSearch");
  if(input && !input.value) input.value="TBZ";
  STP_renderSearchHint();
}

function STP_renderSearchHint(){
  const box=document.getElementById("stpMatches");
  if(box && !box.innerHTML.trim()){
    box.innerHTML='<div style="font-size:8px;color:#64748b;padding:4px">Type a ticker such as TBZ and press Analyze.</div>';
  }
}

function STP_scheduleSearch(){
  clearTimeout(STP_searchTimer);
  const q=String((document.getElementById("stpSearch")||{}).value||"").trim();
  if(q.length<2){STP_renderSearchHint();return}
  STP_searchTimer=setTimeout(function(){STP_searchInternet(q)},350);
}

function STP_searchInternet(q){
  const box=document.getElementById("stpMatches");
  if(!box)return;
  box.innerHTML='<div style="font-size:8px;color:#64748b;padding:4px">Searching internet…</div>';

  google.script.run
    .withSuccessHandler(function(result){
      if(!result || !result.success || !Array.isArray(result.results) || !result.results.length){
        box.innerHTML='<div style="font-size:8px;color:#64748b;padding:4px">No NSE suggestions. You can still press Analyze for the typed symbol.</div>';
        return;
      }
      box.innerHTML=result.results.map(function(x){
        return '<div class="stp-v111-match" onclick="STP_pickSearch(\''+esc(x.symbol)+'\')">'+
          '<b>'+esc(x.symbol)+' · '+esc(x.name||"")+'</b>'+
          '<span>'+esc(x.exchange||"NSE")+' · '+esc(x.type||"Equity")+'</span>'+
        '</div>';
      }).join("");
    })
    .withFailureHandler(function(){
      box.innerHTML='<div style="font-size:8px;color:#64748b;padding:4px">Search suggestions unavailable. Direct symbol analysis still works.</div>';
    })
    .searchInternetStocksForWeb(q);
}

function STP_pickSearch(symbol){
  const input=document.getElementById("stpSearch");
  if(input)input.value=symbol;
  const box=document.getElementById("stpMatches");
  if(box)box.innerHTML="";
  STP_analyzeCurrent(false);
}

function STP_quickAnalyze(symbol){
  const input=document.getElementById("stpSearch");
  if(input)input.value=symbol;
  STP_analyzeCurrent(false);
}

function STP_setLoading(on,text){
  const loader=document.getElementById("stpLoading");
  if(!loader)return;
  loader.style.display=on?"flex":"none";
  const span=loader.querySelector("span");
  if(span && text)span.textContent=text;
}

function STP_analyzeCurrent(forceRefresh){
  const input=document.getElementById("stpSearch");
  const raw=String((input||{}).value||"").trim().toUpperCase();
  if(!raw){alert("Enter an NSE stock ticker.");return}

  STP_setLoading(true,"Downloading market history and calculating indicators…");

  const status=document.getElementById("stpProviderStatus");
  if(status){status.textContent="● Connecting to market data…";status.style.color="#fbbf24"}

  google.script.run
    .withSuccessHandler(function(result){
      STP_setLoading(false);

      if(!result || !result.success){
        const msg=(result&&result.message)||"Could not load market data.";
        if(status){status.textContent="● Market-data error";status.style.color="#fb7185"}
        alert("Could not analyze "+raw+".\n\n"+msg);
        return;
      }

      STP_marketData=result;

      const empty=document.getElementById("stpEmpty");
      const content=document.getElementById("stpContent");
      if(empty)empty.style.display="none";
      if(content)content.style.display="block";

      if(status){
        status.textContent="● "+(result.cached?"Cached":"Internet")+" · "+(result.provider||"Market data");
        status.style.color="#4ade80";
      }

      STP_renderInternetAnalysis();
    })
    .withFailureHandler(function(err){
      STP_setLoading(false);
      if(status){status.textContent="● Connection failed";status.style.color="#fb7185"}
      alert("Internet market-data request failed.\n"+((err&&err.message)||String(err)));
    })
    .getInternetStockForWeb(raw);
}

function STP_num(v){const n=Number(v);return isFinite(n)?n:null}
function STP_money(v){
  if(v==null||!isFinite(v))return "—";
  return "₹"+Number(v).toLocaleString("en-IN",{minimumFractionDigits:2,maximumFractionDigits:2});
}
function STP_pct(v){
  if(v==null||!isFinite(v))return "—";
  return (v>=0?"+":"")+Number(v).toFixed(2)+"%";
}
function STP_sma(arr,n){
  if(!arr||arr.length<n)return null;
  let s=0;for(let i=arr.length-n;i<arr.length;i++)s+=arr[i];
  return s/n;
}
function STP_smaSeries(arr,n){
  const out=new Array(arr.length).fill(null);
  let sum=0;
  for(let i=0;i<arr.length;i++){
    sum+=arr[i];
    if(i>=n)sum-=arr[i-n];
    if(i>=n-1)out[i]=sum/n;
  }
  return out;
}
function STP_emaSeries(arr,n){
  if(!arr||!arr.length)return [];
  const out=new Array(arr.length).fill(null);
  const k=2/(n+1);
  let ema=arr[0];
  out[0]=ema;
  for(let i=1;i<arr.length;i++){ema=arr[i]*k+ema*(1-k);out[i]=ema}
  return out;
}
function STP_ema(arr,n){
  const s=STP_emaSeries(arr,n);return s.length?s[s.length-1]:null;
}
function STP_std(a){
  if(!a.length)return 0;
  const m=a.reduce((s,x)=>s+x,0)/a.length;
  return Math.sqrt(a.reduce((s,x)=>s+Math.pow(x-m,2),0)/a.length);
}
function STP_bollinger(arr,n){
  if(arr.length<n)return null;
  const a=arr.slice(-n),mid=a.reduce((s,x)=>s+x,0)/n,sd=STP_std(a);
  return {mid:mid,upper:mid+2*sd,lower:mid-2*sd};
}
function STP_rsi(arr,n){
  if(arr.length<n+1)return null;
  const changes=[];
  for(let i=1;i<arr.length;i++)changes.push(arr[i]-arr[i-1]);
  let gains=0,losses=0;
  for(let i=0;i<n;i++){gains+=Math.max(changes[i],0);losses+=Math.max(-changes[i],0)}
  let avgGain=gains/n,avgLoss=losses/n;
  for(let i=n;i<changes.length;i++){
    avgGain=(avgGain*(n-1)+Math.max(changes[i],0))/n;
    avgLoss=(avgLoss*(n-1)+Math.max(-changes[i],0))/n;
  }
  if(avgLoss===0)return 100;
  return 100-(100/(1+avgGain/avgLoss));
}
function STP_atr(rows,n){
  if(rows.length<n+1)return null;
  const tr=[];
  for(let i=1;i<rows.length;i++){
    const h=rows[i].high,l=rows[i].low,pc=rows[i-1].close;
    tr.push(Math.max(h-l,Math.abs(h-pc),Math.abs(l-pc)));
  }
  let atr=tr.slice(0,n).reduce((s,x)=>s+x,0)/n;
  for(let i=n;i<tr.length;i++)atr=(atr*(n-1)+tr[i])/n;
  return atr;
}
function STP_macd(arr){
  if(arr.length<35)return null;
  const e12=STP_emaSeries(arr,12),e26=STP_emaSeries(arr,26);
  const macd=arr.map((_,i)=>e12[i]-e26[i]);
  const signal=STP_emaSeries(macd.slice(25),9);
  const m=macd[macd.length-1];
  const s=signal[signal.length-1];
  return {macd:m,signal:s,hist:m-s};
}
function STP_adx(rows,n){
  if(rows.length<n*2+2)return null;
  const tr=[],plusDM=[],minusDM=[];
  for(let i=1;i<rows.length;i++){
    const up=rows[i].high-rows[i-1].high;
    const dn=rows[i-1].low-rows[i].low;
    plusDM.push(up>dn&&up>0?up:0);
    minusDM.push(dn>up&&dn>0?dn:0);
    tr.push(Math.max(rows[i].high-rows[i].low,Math.abs(rows[i].high-rows[i-1].close),Math.abs(rows[i].low-rows[i-1].close)));
  }
  let atr=tr.slice(0,n).reduce((s,x)=>s+x,0);
  let p=plusDM.slice(0,n).reduce((s,x)=>s+x,0);
  let m=minusDM.slice(0,n).reduce((s,x)=>s+x,0);
  const dx=[];
  for(let i=n;i<tr.length;i++){
    atr=atr-atr/n+tr[i];p=p-p/n+plusDM[i];m=m-m/n+minusDM[i];
    const pdi=100*(p/atr),mdi=100*(m/atr),den=pdi+mdi;
    if(den)dx.push(100*Math.abs(pdi-mdi)/den);
  }
  if(dx.length<n)return null;
  let adx=dx.slice(0,n).reduce((s,x)=>s+x,0)/n;
  for(let i=n;i<dx.length;i++)adx=(adx*(n-1)+dx[i])/n;
  return adx;
}
function STP_supertrend(rows,period,mult){
  if(rows.length<period+2)return null;
  const trs=[];
  for(let i=1;i<rows.length;i++){
    trs.push(Math.max(rows[i].high-rows[i].low,Math.abs(rows[i].high-rows[i-1].close),Math.abs(rows[i].low-rows[i-1].close)));
  }
  let atr=trs.slice(0,period).reduce((s,x)=>s+x,0)/period;
  const atrs=new Array(rows.length).fill(null);
  atrs[period]=atr;
  for(let i=period+1;i<rows.length;i++){
    atr=(atr*(period-1)+trs[i-1])/period;atrs[i]=atr;
  }
  let finalUpper=null,finalLower=null,st=null,trend=1;
  for(let i=period;i<rows.length;i++){
    const hl2=(rows[i].high+rows[i].low)/2;
    const upper=hl2+mult*atrs[i],lower=hl2-mult*atrs[i];
    if(i===period){finalUpper=upper;finalLower=lower;st=finalLower;trend=1;continue}
    finalUpper=(upper<finalUpper||rows[i-1].close>finalUpper)?upper:finalUpper;
    finalLower=(lower>finalLower||rows[i-1].close<finalLower)?lower:finalLower;
    if(st===finalUpper && rows[i].close>finalUpper){trend=1;st=finalLower}
    else if(st===finalLower && rows[i].close<finalLower){trend=-1;st=finalUpper}
    else st=trend===1?finalLower:finalUpper;
  }
  return {value:st,trend:trend};
}
function STP_returns(arr,n){
  if(arr.length<=n)return null;
  const old=arr[arr.length-1-n],now=arr[arr.length-1];
  return old?((now/old)-1)*100:null;
}
function STP_upDays(arr,n){
  let up=0,total=0;
  for(let i=Math.max(1,arr.length-n);i<arr.length;i++){if(arr[i]>arr[i-1])up++;total++}
  return {up:up,total:total};
}
function STP_recentSupportResistance(rows,n){
  const r=rows.slice(-Math.min(n,rows.length));
  return {
    support:Math.min.apply(null,r.map(x=>x.low)),
    resistance:Math.max.apply(null,r.map(x=>x.high))
  };
}
function STP_volumeRatio(rows,n){
  const r=rows.slice(-Math.min(n,rows.length));
  if(r.length<2)return null;
  const latest=r[r.length-1].volume||0;
  const prev=r.slice(0,-1).map(x=>x.volume||0).filter(x=>x>0);
  if(!prev.length)return null;
  const avg=prev.reduce((s,x)=>s+x,0)/prev.length;
  return avg?latest/avg:null;
}

function STP_computeInternet(){
  if(!STP_marketData||!Array.isArray(STP_marketData.history))return null;
  const rows=STP_marketData.history.map(x=>({
    date:x.date,displayDate:x.displayDate,
    open:Number(x.open),high:Number(x.high),low:Number(x.low),close:Number(x.close),volume:Number(x.volume)||0
  })).filter(x=>isFinite(x.close)&&x.close>0);
  const closes=rows.map(x=>x.close);
  if(closes.length<20)return null;

  const latest=Number(STP_marketData.marketPrice)||closes[closes.length-1];
  const previous=Number(STP_marketData.previousClose)||closes[closes.length-2];
  const sma20=STP_sma(closes,20),sma50=STP_sma(closes,50),sma200=STP_sma(closes,200);
  const ema9=STP_ema(closes,9),ema20=STP_ema(closes,20),ema50=STP_ema(closes,50);
  const rsi=STP_rsi(closes,14),bb=STP_bollinger(closes,20),macd=STP_macd(closes);
  const atr=STP_atr(rows,14),adx=STP_adx(rows,14),supertrend=STP_supertrend(rows,10,3);
  const mom20=STP_returns(closes,20),up20=STP_upDays(closes,20);
  const year=rows.slice(-252),hi52=Math.max.apply(null,year.map(x=>x.high)),lo52=Math.min.apply(null,year.map(x=>x.low));
  const nearHigh=hi52?latest/hi52*100:0;
  const sr=STP_recentSupportResistance(rows,20);
  const volRatio=STP_volumeRatio(rows,20);

  let mediumScore=0,swingScore=0;
  const medium=[],swing=[];

  function add(list,type,text){list.push({type:type,text:text})}

  if(sma50!=null&&latest>sma50){mediumScore+=2;add(medium,"good","Price is above SMA 50 — medium-term trend is bullish.")}
  else if(sma50!=null){mediumScore-=2;add(medium,"bad","Price is below SMA 50 — medium-term trend is weak.")}

  if(sma200!=null&&sma50!=null&&sma50>sma200){mediumScore+=2;add(medium,"good","SMA 50 is above SMA 200 — long-term structure is bullish.")}
  else if(sma200!=null&&sma50!=null){mediumScore-=1;add(medium,"bad","SMA 50 is below SMA 200 — long-term structure is not aligned.")}

  if(adx!=null&&adx>=25){mediumScore+=1;add(medium,"good","ADX "+adx.toFixed(1)+" indicates a meaningful trend.")}
  else if(adx!=null)add(medium,"warn","ADX "+adx.toFixed(1)+" indicates a weak / developing trend.");

  if(nearHigh>=95){mediumScore+=1;add(medium,"good","Price is trading near its 52-week high ("+nearHigh.toFixed(1)+"% of high).")}
  else if(nearHigh<75){mediumScore-=1;add(medium,"warn","Price is materially below its 52-week high ("+nearHigh.toFixed(1)+"% of high).")}

  if(supertrend){
    if(supertrend.trend>0){mediumScore+=1;swingScore+=1;add(medium,"good","Supertrend is bullish.");add(swing,"good","Supertrend remains bullish.")}
    else{mediumScore-=1;swingScore-=1;add(medium,"bad","Supertrend is bearish.");add(swing,"bad","Supertrend is bearish.")}
  }

  if(ema9!=null&&latest>ema9){swingScore+=2;add(swing,"good","Price is above EMA 9 — short-term momentum is positive.")}
  else if(ema9!=null){swingScore-=2;add(swing,"bad","Price is below EMA 9 — short-term momentum is weak.")}

  if(ema9!=null&&ema20!=null&&ema9>ema20){swingScore+=1;add(swing,"good","EMA 9 is above EMA 20 — bullish short-term alignment.")}
  else if(ema9!=null&&ema20!=null){swingScore-=1;add(swing,"bad","EMA 9 is below EMA 20.")}

  if(rsi!=null){
    if(rsi>=55&&rsi<=70){swingScore+=1;add(swing,"good","RSI "+rsi.toFixed(1)+" supports positive momentum without being extremely overbought.")}
    else if(rsi>70){add(swing,"warn","RSI "+rsi.toFixed(1)+" is overbought — momentum is strong but pullback risk is higher.")}
    else if(rsi<40){swingScore-=1;add(swing,"bad","RSI "+rsi.toFixed(1)+" shows weak momentum.")}
    else add(swing,"warn","RSI "+rsi.toFixed(1)+" is neutral.");
  }

  if(macd){
    if(macd.hist>0){swingScore+=1;add(swing,"good","MACD histogram is positive — momentum confirmation.")}
    else{swingScore-=1;add(swing,"bad","MACD histogram is negative — momentum is not confirmed.")}
  }

  if(bb){
    if(latest>bb.upper){swingScore+=1;add(swing,"warn","Price is above the upper Bollinger Band — breakout / volatility expansion.")}
    else if(latest<bb.lower){swingScore-=1;add(swing,"bad","Price is below the lower Bollinger Band — downside pressure.")}
    else add(swing,"good","Price is trading inside Bollinger Bands.");
  }

  if(volRatio!=null){
    if(volRatio>=1.3){swingScore+=1;add(swing,"good","Latest volume is "+volRatio.toFixed(2)+"× the recent average — participation is elevated.")}
    else add(swing,"warn","Latest volume is "+volRatio.toFixed(2)+"× the recent average.");
  }

  const risk=Math.max(atr||0,latest*0.02);
  let stop=Math.min(latest-risk*1.5,sr.support*0.995);
  if(!isFinite(stop)||stop<=0||stop>=latest)stop=latest-risk*1.5;
  const riskPerShare=latest-stop;
  const t1=latest+riskPerShare*1.5;
  const t2=latest+riskPerShare*3;

  return {
    rows,closes,latest,previous,sma20,sma50,sma200,ema9,ema20,ema50,rsi,bb,macd,atr,adx,supertrend,
    mom20,up20,hi52,lo52,nearHigh,support:sr.support,resistance:sr.resistance,volRatio,
    mediumScore,swingScore,medium,swing,stop,t1,t2,riskPerShare
  };
}

function STP_rec(score,type){
  if(type==="medium"){
    if(score>=5)return ["STRONG ACCUMULATE","strong","Broad trend conditions are strongly aligned for the medium-term technical setup."];
    if(score>=2)return ["ACCUMULATE / BUY ON DIPS","buy","The broader technical structure is constructive, with some conditions still needing confirmation."];
    if(score>=0)return ["WATCH","watch","Signals are mixed. A stronger trend or momentum confirmation would improve the setup."];
    return ["WEAK / AVOID","avoid","The current medium-term technical structure is unfavorable."];
  }
  if(score>=4)return ["SWING BUY","strong","Short-term trend and momentum conditions are strongly aligned."];
  if(score>=2)return ["SWING BUY / WATCH","buy","There is a positive short-term setup, but confirmation and disciplined risk control remain important."];
  if(score>=0)return ["NEUTRAL","neutral","The short-term setup is mixed with no strong technical edge."];
  return ["AVOID / WAIT","avoid","Short-term technical conditions are currently weak."];
}

function STP_set(id,text,cls){
  const e=document.getElementById(id);if(!e)return;
  e.textContent=text;
  if(cls)e.className=cls;
}
function STP_factorHTML(list){
  return list.map(x=>'<div class="stp-v111-factor '+x.type+'">• '+esc(x.text)+'</div>').join("");
}

function STP_renderInternetAnalysis(){
  const a=STP_computeInternet();
  if(!a)return;

  const d=STP_marketData;
  STP_set("stpSymbol",d.symbol||d.yahooSymbol||"—");
  STP_set("stpExchange",d.exchangeName||"NSE");
  STP_set("stpCompany","Internet market-data analysis · "+(d.currency||"INR")+" · "+(d.provider||"Provider"));
  STP_set("stpLatestDate",a.rows[a.rows.length-1].displayDate||a.rows[a.rows.length-1].date);
  STP_set("stpPrice",STP_money(a.latest));
  STP_set("stpDayChange",STP_pct(d.dayChangePct),d.dayChangePct>=0?"stp-pos":"stp-neg");
  STP_set("stpRange",STP_money(a.lo52)+" – "+STP_money(a.hi52));
  STP_set("stpNearHigh",a.nearHigh.toFixed(1)+"% of 52W high");
  STP_set("stpRsi",a.rsi==null?"—":a.rsi.toFixed(1));
  STP_set("stpRsiText",a.rsi==null?"Insufficient history":a.rsi>70?"Overbought":a.rsi<30?"Oversold":a.rsi>=55?"Bullish momentum":"Neutral / weak");

  const totalScore=a.mediumScore+a.swingScore;
  const consensus=totalScore>=7?"STRONG BUY":totalScore>=3?"BUY":totalScore>=0?"NEUTRAL":"WEAK";
  STP_set("stpConsensus",consensus,totalScore>=3?"stp-pos":totalScore<0?"stp-neg":"stp-warn-text");
  STP_set("stpScore","Technical score: "+(totalScore>=0?"+":"")+totalScore);
  STP_set("stpMom20",STP_pct(a.mom20),a.mom20>=0?"stp-pos":"stp-neg");
  STP_set("stpMomText",a.mom20>=5?"Strong positive momentum":a.mom20>=0?"Positive momentum":"Negative momentum");

  const m=STP_rec(a.mediumScore,"medium"),s=STP_rec(a.swingScore,"swing");
  const mb=document.getElementById("stpMediumBadge");if(mb){mb.textContent=m[0];mb.className="stp-v111-rec "+m[1]}
  const sb=document.getElementById("stpSwingBadge");if(sb){sb.textContent=s[0];sb.className="stp-v111-rec "+s[1]}
  STP_set("stpMediumText",m[2]);STP_set("stpSwingText",s[2]);
  document.getElementById("stpMediumFactors").innerHTML=STP_factorHTML(a.medium);
  document.getElementById("stpSwingFactors").innerHTML=STP_factorHTML(a.swing);

  STP_set("stpEntry",STP_money(a.latest));
  STP_set("stpSL",STP_money(a.stop),"stp-neg");
  STP_set("stpSLPct",STP_pct((a.stop/a.latest-1)*100),"stp-neg");
  STP_set("stpT1",STP_money(a.t1),"stp-pos");
  STP_set("stpT1Pct",STP_pct((a.t1/a.latest-1)*100),"stp-pos");
  STP_set("stpT2",STP_money(a.t2),"stp-pos");
  STP_set("stpT2Pct",STP_pct((a.t2/a.latest-1)*100),"stp-pos");
  STP_set("stpRR","1 : 3.0","stp-pos");

  function ma(v,idv,ids){
    STP_set(idv,STP_money(v));
    if(v==null)STP_set(ids,"Insufficient history");
    else STP_set(ids,a.latest>v?"Price above":"Price below",a.latest>v?"stp-pos":"stp-neg");
  }
  ma(a.sma20,"stpSma20v","stpSma20s");ma(a.sma50,"stpSma50v","stpSma50s");ma(a.sma200,"stpSma200v","stpSma200s");
  STP_set("stpEmaPair",(a.ema9==null||a.ema20==null)?"—":STP_money(a.ema9)+" / "+STP_money(a.ema20));
  STP_set("stpEmaSignal",(a.ema9!=null&&a.ema20!=null&&a.ema9>a.ema20)?"Bullish alignment":"Weak / bearish alignment",(a.ema9!=null&&a.ema20!=null&&a.ema9>a.ema20)?"stp-pos":"stp-neg");
  STP_set("stpMacd",a.macd==null?"—":a.macd.hist.toFixed(2));
  STP_set("stpMacdSignal",a.macd==null?"Insufficient history":a.macd.hist>0?"Positive histogram":"Negative histogram",a.macd&&a.macd.hist>0?"stp-pos":"stp-neg");
  STP_set("stpAdx",a.adx==null?"—":a.adx.toFixed(1));
  STP_set("stpAdxText",a.adx==null?"Insufficient history":a.adx>=25?"Strong trend":"Weak / developing trend",a.adx>=25?"stp-pos":"stp-warn-text");
  STP_set("stpAtr",STP_money(a.atr));
  STP_set("stpAtrText",a.atr==null?"Insufficient history":"Daily volatility ~"+((a.atr/a.latest)*100).toFixed(2)+"%");
  STP_set("stpSupertrend",a.supertrend==null?"—":a.supertrend.trend>0?"BULLISH":"BEARISH",a.supertrend&&a.supertrend.trend>0?"stp-pos":"stp-neg");
  STP_set("stpSupertrendText",a.supertrend==null?"Insufficient history":STP_money(a.supertrend.value));
  if(a.bb){
    const p=a.latest>a.bb.upper?"Above Upper":a.latest<a.bb.lower?"Below Lower":"Inside Bands";
    STP_set("stpBoll",p,p==="Above Upper"?"stp-pos":p==="Below Lower"?"stp-neg":"");
    STP_set("stpBollText","Upper "+STP_money(a.bb.upper)+" · Lower "+STP_money(a.bb.lower));
  }
  STP_set("stpUpDays",a.up20.total?a.up20.up+"/"+a.up20.total:"—");
  STP_set("stpUpText",a.up20.total?((a.up20.up/a.up20.total)*100).toFixed(0)+"% positive sessions":"—");
  STP_set("stpSupportV",STP_money(a.support));
  STP_set("stpResistanceV",STP_money(a.resistance));

  STP_drawInternetChart();
}

function STP_drawInternetChart(){
  const a=STP_computeInternet(),svg=document.getElementById("stpChart");
  if(!a||!svg)return;

  const n=Math.max(22,Number((document.getElementById("stpWindow")||{}).value||252));
  const rows=a.rows.slice(-n),closes=rows.map(x=>x.close);
  const fullCloses=a.closes;
  const fullStart=a.rows.length-rows.length;

  const s20=STP_smaSeries(fullCloses,20).slice(fullStart);
  const s50=STP_smaSeries(fullCloses,50).slice(fullStart);
  const s200=STP_smaSeries(fullCloses,200).slice(fullStart);
  const e9=STP_emaSeries(fullCloses,9).slice(fullStart);

  let bu=new Array(rows.length).fill(null),bl=new Array(rows.length).fill(null);
  for(let i=0;i<rows.length;i++){
    const globalIndex=fullStart+i;
    if(globalIndex>=19){
      const part=fullCloses.slice(0,globalIndex+1),b=STP_bollinger(part,20);
      bu[i]=b.upper;bl[i]=b.lower;
    }
  }

  const values=closes.slice();
  [s20,s50,s200,e9,bu,bl].forEach(s=>s.forEach(v=>{if(v!=null&&isFinite(v))values.push(v)}));
  if((document.getElementById("stpSupport")||{}).checked){values.push(a.support,a.resistance)}
  let min=Math.min.apply(null,values),max=Math.max.apply(null,values);
  const pad=(max-min)*.08||1;min-=pad;max+=pad;

  const W=1280,H=470,L=62,R=24,T=22,B=42;
  const x=i=>L+(i/(Math.max(1,rows.length-1)))*(W-L-R);
  const y=v=>T+(max-v)/(max-min)*(H-T-B);

  function poly(series,color,width,dash,opacity){
    const pts=[];
    series.forEach((v,i)=>{if(v!=null&&isFinite(v))pts.push(x(i).toFixed(1)+","+y(v).toFixed(1))});
    if(pts.length<2)return "";
    return '<polyline points="'+pts.join(" ")+'" fill="none" stroke="'+color+'" stroke-width="'+width+'" stroke-linejoin="round" stroke-linecap="round"'+(dash?' stroke-dasharray="'+dash+'"':'')+' opacity="'+(opacity||1)+'"/>';
  }

  let out='';
  for(let i=0;i<5;i++){
    const yy=T+i*(H-T-B)/4,val=max-i*(max-min)/4;
    out+='<line x1="'+L+'" y1="'+yy+'" x2="'+(W-R)+'" y2="'+yy+'" stroke="#1d2939" stroke-width="1"/>';
    out+='<text x="8" y="'+(yy+4)+'" fill="#64748b" font-size="12">₹'+val.toFixed(1)+'</text>';
  }

  // soft area under price
  const areaPts=closes.map((v,i)=>x(i).toFixed(1)+","+y(v).toFixed(1));
  if(areaPts.length){
    const area='M '+x(0)+' '+(H-B)+' L '+areaPts.join(' L ')+' L '+x(closes.length-1)+' '+(H-B)+' Z';
    out+='<path d="'+area+'" fill="#2563eb" opacity=".08"/>';
  }

  if((document.getElementById("stpBb")||{}).checked){
    out+=poly(bu,"#64748b",1.2,"6 6",.85);out+=poly(bl,"#64748b",1.2,"6 6",.85);
  }
  if((document.getElementById("stpSma200")||{}).checked)out+=poly(s200,"#f97316",1.7,"",.9);
  if((document.getElementById("stpSma50")||{}).checked)out+=poly(s50,"#a78bfa",1.8,"",.95);
  if((document.getElementById("stpSma20")||{}).checked)out+=poly(s20,"#f59e0b",1.8,"",.95);
  if((document.getElementById("stpEma9")||{}).checked)out+=poly(e9,"#22c55e",1.8,"",.95);
  out+=poly(closes,"#60a5fa",3,"",1);

  if((document.getElementById("stpSupport")||{}).checked){
    [['Support',a.support,'#22c55e'],['Resistance',a.resistance,'#ef4444']].forEach(function(z){
      const yy=y(z[1]);out+='<line x1="'+L+'" y1="'+yy+'" x2="'+(W-R)+'" y2="'+yy+'" stroke="'+z[2]+'" stroke-width="1.3" stroke-dasharray="7 5" opacity=".75"/>';
      out+='<text x="'+(W-R-6)+'" y="'+(yy-5)+'" fill="'+z[2]+'" text-anchor="end" font-size="11">'+z[0]+' '+STP_money(z[1])+'</text>';
    });
  }

  const every=Math.max(1,Math.floor(rows.length/6));
  rows.forEach(function(p,i){
    if(i%every===0||i===rows.length-1){
      out+='<text x="'+x(i)+'" y="'+(H-14)+'" fill="#64748b" font-size="11" text-anchor="middle">'+esc(p.displayDate||p.date)+'</text>';
    }
  });

  // Last price marker
  const ly=y(closes[closes.length-1]);
  out+='<circle cx="'+x(closes.length-1)+'" cy="'+ly+'" r="4.5" fill="#60a5fa"/>';
  out+='<text x="'+(W-R-3)+'" y="'+(ly-9)+'" fill="#93c5fd" text-anchor="end" font-size="12" font-weight="700">'+STP_money(closes[closes.length-1])+'</text>';

  svg.innerHTML=out;
}

function ST_open(){
  // Stocks page opens as an icon hub. Data loads only after ₹100 Scanner is clicked.
  ST_closeTools();
}

function showPage(id,btn){
  document.querySelectorAll(".page").forEach(function(x){x.classList.remove("active")});
  const page=document.getElementById(id);
  if(page)page.classList.add("active");

  document.querySelectorAll(".nav").forEach(function(x){x.classList.remove("active")});
  if(btn)btn.classList.add("active");

  if(id==="money"){
    if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
    if(typeof renderMoneyQuickEntry==="function")renderMoneyQuickEntry();

    // Always re-read the help sheet when Money is opened so new items
    // such as Zerodha / Angel One appear without editing the HTML.
    if(typeof refreshMoneyCategories==="function"){
      refreshMoneyCategories(false).catch(function(){});
    }
  }
  if(id==="stocks" && typeof ST_open==="function")ST_open();

  if(id==="time"){
    if(typeof TB_renderAll==="function")TB_renderAll();
    document.querySelectorAll(".tb-tool-panel").forEach(function(p){p.classList.remove("tb-tool-open")});
    document.querySelectorAll(".tb-command-btn").forEach(function(b){b.classList.remove("active")});
  }

  if(id==="health" && typeof HL_renderAll==="function")HL_renderAll();
  if(id==="learning" && typeof LR_render==="function")LR_render();

  if(id==="review"){
    setTimeout(function(){RV_openReview()},0);
  }
}
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]})}



function confirmSheetUpload(fileName,rowCount){
  localStorage.setItem("lastSheetUploadMessage",JSON.stringify({
    file:fileName,
    count:rowCount,
    time:new Date().toISOString()
  }));
  closeUploadWindow();
  updateMoneyDashboard();
  alert("✓ Sheet has been uploaded successfully.");
}

function openSheetDataWindow(){
  document.getElementById("sheetDataWindow").style.display="flex";
  renderSheetDataWindow();
}
function closeSheetDataWindow(){
  document.getElementById("sheetDataWindow").style.display="none";
}
function renderSheetDataWindow(){
  const data=JSON.parse(localStorage.getItem("moneyEntries")||"[]").filter(x=>x.source==="google-sheet" || x.source==="sheet");
  const status=document.getElementById("sheetDataStatus");
  const table=document.getElementById("sheetDataTable");
  if(!status||!table)return;

  if(!data.length){
    status.textContent="No sheet imported yet.";
    table.innerHTML='<p class="muted">Upload a sheet from Money → Upload Data → Sheet Upload.</p>';
    return;
  }

  const last=JSON.parse(localStorage.getItem("lastSheetUploadMessage")||"null");
  status.textContent=last
    ? "✓ "+last.count+" sheet transactions uploaded from "+last.file+"."
    : "✓ "+data.length+" sheet transactions loaded.";

  const recent=[...data].reverse();
  table.innerHTML='<div style="overflow:auto;margin-top:14px"><table style="width:100%;border-collapse:collapse;font-size:13px"><thead><tr>'+
    '<th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Date</th>'+
    '<th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Main Category</th>'+
    '<th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Sub Category</th>'+
    '<th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Explanation</th>'+
    '<th style="text-align:right;padding:8px;border-bottom:1px solid #ddd">Amount</th>'+
    '<th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Account</th>'+
    '</tr></thead><tbody>'+
    recent.map(x=>'<tr>'+
      '<td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.date||"")+'</td>'+
      '<td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.mainCategory||"")+'</td>'+
      '<td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.subCategory||"")+'</td>'+
      '<td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.explanation||"")+'</td>'+
      '<td style="padding:8px;border-bottom:1px solid #eee;text-align:right">'+moneyFmt(activeMoneyCategoryView==="Savings" ? savingsSignedAmount(x) : x.amount)+'</td>'+
      '<td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.account||x.fromAccount||"")+'</td>'+
    '</tr>').join('')+
    '</tbody></table></div>';
}



function openMoneyOthers(){
  document.getElementById("moneyOthersWindow").style.display="flex";
}
function closeMoneyOthers(){
  document.getElementById("moneyOthersWindow").style.display="none";
}

function openMoneySet(){
  document.getElementById("moneySetWindow").style.display="flex";
  renderMoneySet();
  syncMoneySetFromGoogleSheet(false).catch(function(){});
}
function closeMoneySet(){
  document.getElementById("moneySetWindow").style.display="none";
}
let openMoneySetCategory = "";

function renderMoneySet(){
  const body=document.getElementById("moneySetBody");
  if(!body)return;

  const groups=Object.keys(config.categories);

  if(!openMoneySetCategory && groups.length){
    openMoneySetCategory=groups[0];
  }

  const topTabs=
    '<div class="money-set-main-tabs">'+
      groups.map(function(group){
        return '<button class="money-set-main-tab '+(openMoneySetCategory===group?"active":"")+'" onclick="selectMoneySetCategory(\''+esc(group).replace(/'/g,"&#39;")+'\')">'+
          '<b>'+esc(group)+'</b>'+
          '<span>'+(config.categories[group]||[]).length+' sub categories</span>'+
        '</button>';
      }).join('')+
    '</div>';

  const selected=openMoneySetCategory;
  const items=config.categories[selected]||[];

  const detail = selected ? (
    '<div class="set-main-group money-set-detail">'+
      '<div class="set-main-head">'+
        '<div>'+
          '<div class="set-main-title">'+esc(selected)+'</div>'+
          '<div class="muted">'+items.length+' sub categories</div>'+
        '</div>'+
        '<div class="set-main-actions">'+
          '<button class="rename-btn" onclick="renameMainCategory(\''+esc(selected).replace(/'/g,"&#39;")+'\')">Rename</button>'+
          '<button class="delete-main-btn" onclick="deleteMainCategory(\''+esc(selected).replace(/'/g,"&#39;")+'\')">Delete</button>'+
        '</div>'+
      '</div>'+
      '<div class="money-set-sub-list">'+
        items.map(function(item,i){
          return '<div class="set-sub-row">'+
            '<input value="'+esc(item)+'" onchange="renameSubCategory(\''+esc(selected).replace(/'/g,"&#39;")+'\','+i+',this.value)">'+
            '<button class="remove" onclick="removeSetSubCategory(\''+esc(selected).replace(/'/g,"&#39;")+'\','+i+')">Delete</button>'+
          '</div>';
        }).join('')+
      '</div>'+
      '<div class="set-add-sub">'+
        '<input id="setAdd_'+safeId(selected)+'" placeholder="Add sub category under '+esc(selected)+'">'+
        '<button onclick="addSetSubCategory(\''+esc(selected).replace(/'/g,"&#39;")+'\')">＋ Add</button>'+
      '</div>'+
    '</div>'
  ) : '';

  body.innerHTML=topTabs+detail;

  const acc=document.getElementById("setAccountsBody");
  if(acc){
    acc.innerHTML=config.accounts.map(function(a,i){
      return '<div class="set-sub-row">'+
        '<input value="'+esc(a)+'" onchange="renameSetAccount('+i+',this.value)">'+
        '<button class="remove" onclick="removeSetAccount('+i+')">Delete</button>'+
      '</div>';
    }).join('');
  }
}

function selectMoneySetCategory(group){
  openMoneySetCategory=group;
  renderMoneySet();
}

function safeId(s){return String(s).replace(/[^a-zA-Z0-9]/g,"_")}
function saveSetConfig(){
  localStorage.setItem("moneyConfig",JSON.stringify(config));

  // Debounce to avoid multiple writes while the user is editing quickly.
  if(moneySetSaveTimer)clearTimeout(moneySetSaveTimer);
  moneySetSaveTimer=setTimeout(function(){
    pushMoneySetToGoogleSheet();
  },400);
}
function addSetSubCategory(group){
  const el=document.getElementById("setAdd_"+safeId(group));
  if(!el)return;
  const v=el.value.trim();
  if(!v)return;
  if(!config.categories[group])config.categories[group]=[];
  if(!config.categories[group].includes(v))config.categories[group].push(v);
  saveSetConfig();
  renderMoneySet();
}
function renameSubCategory(group,index,value){
  const v=String(value).trim();
  if(!v){renderMoneySet();return;}
  config.categories[group][index]=v;
  saveSetConfig();
}
function removeSetSubCategory(group,index){
  if(!confirm("Delete this sub category?"))return;
  config.categories[group].splice(index,1);
  saveSetConfig();
  renderMoneySet();
}
function addMainCategory(){
  const el=document.getElementById("newMainCategoryName");
  const v=el.value.trim();
  if(!v)return;
  if(config.categories[v]){
    alert("This main category already exists.");
    return;
  }
  config.categories[v]=[];
  openMoneySetCategory=v;
  saveSetConfig();
  renderMoneySet();
}
function renameMainCategory(oldName){
  const newName=prompt("New name for "+oldName+":",oldName);
  if(!newName || newName.trim()===oldName)return;
  const n=newName.trim();
  if(config.categories[n]){
    alert("A main category with this name already exists.");
    return;
  }
  config.categories[n]=config.categories[oldName];
  delete config.categories[oldName];
  if(openMoneySetCategory===oldName)openMoneySetCategory=n;

  // Update saved transactions so the whole website stays consistent.
  const data=JSON.parse(localStorage.getItem("moneyEntries")||"[]");
  data.forEach(function(x){
    if(x.mainCategory===oldName)x.mainCategory=n;
  });
  localStorage.setItem("moneyEntries",JSON.stringify(data));

  saveSetConfig();
  updateMoneyDashboard();
  renderMoneySet();
}
function deleteMainCategory(group){
  if(!confirm("Delete main category '"+group+"' and its sub categories?\nExisting transactions will remain but may no longer match a configured category."))return;
  delete config.categories[group];
  if(openMoneySetCategory===group){
    openMoneySetCategory=Object.keys(config.categories)[0]||"";
  }
  saveSetConfig();
  renderMoneySet();
}
function setAddAccount(){
  const el=document.getElementById("setNewAccount");
  const v=el.value.trim();
  if(!v)return;
  if(!config.accounts.includes(v))config.accounts.push(v);
  saveSetConfig();
  renderMoneySet();
}
function renameSetAccount(index,value){
  const v=String(value).trim();
  if(!v){renderMoneySet();return;}
  config.accounts[index]=v;
  saveSetConfig();
}
function removeSetAccount(index){
  if(!confirm("Delete this account from future dropdowns?"))return;
  config.accounts.splice(index,1);
  saveSetConfig();
  renderMoneySet();
}

function openViewOptions(){
  document.getElementById("viewOptionsWindow").style.display="flex";
  document.getElementById("viewModeChooser").style.display="grid";
  document.getElementById("viewModeContent").innerHTML="";
}
function closeViewOptions(){
  document.getElementById("viewOptionsWindow").style.display="none";
}
function backToViewOptions(){
  document.getElementById("viewModeChooser").style.display="grid";
  document.getElementById("viewModeContent").innerHTML="";
}

/* ---------------- OPTION 1: Previous detailed report ---------------- */

/* Core date/category helpers used by all View Options */
function localDateValue(d){
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
}

function parseTrackerDate(v){
  if(v===null || v===undefined || v==="")return null;

  // Apps Script may supply a Date-like value.
  if(Object.prototype.toString.call(v)==="[object Date]"){
    if(isNaN(v.getTime()))return null;
    return new Date(v.getFullYear(),v.getMonth(),v.getDate(),12,0,0);
  }

  const s=String(v).trim();

  // IMPORTANT: Sheet display format is DD-MM-YYYY / DD/MM/YYYY.
  // Parse manually so JavaScript never guesses MM-DD-YYYY.
  let m=s.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
  if(m){
    const dd=Number(m[1]), mm=Number(m[2]), yyyy=Number(m[3]);
    const d=new Date(yyyy,mm-1,dd,12,0,0);
    if(d.getFullYear()===yyyy && d.getMonth()===mm-1 && d.getDate()===dd)return d;
    return null;
  }

  // Google Sheet display format can also be DD-MMM-YYYY, e.g. 10-Sep-2026.
  m=s.match(/^(\d{1,2})[-\s]([A-Za-z]{3,9})[-\s](\d{4})$/);
  if(m){
    const monthMap={
      jan:0,january:0,feb:1,february:1,mar:2,march:2,apr:3,april:3,
      may:4,jun:5,june:5,jul:6,july:6,aug:7,august:7,
      sep:8,september:8,oct:9,october:9,nov:10,november:10,dec:11,december:11
    };
    const dd=Number(m[1]), key=String(m[2]).toLowerCase(), yyyy=Number(m[3]);
    const mm=monthMap[key];
    if(mm!==undefined){
      const d=new Date(yyyy,mm,dd,12,0,0);
      if(d.getFullYear()===yyyy && d.getMonth()===mm && d.getDate()===dd)return d;
    }
    return null;
  }

  // Apps Script / JSON ISO dates: YYYY-MM-DD...
  m=s.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if(m){
    const yyyy=Number(m[1]), mm=Number(m[2]), dd=Number(m[3]);
    const d=new Date(yyyy,mm-1,dd,12,0,0);
    if(d.getFullYear()===yyyy && d.getMonth()===mm-1 && d.getDate()===dd)return d;
    return null;
  }

  // Never ask JavaScript to guess an ambiguous date.
  return null;
}


function displayTrackerDate(v){
  const d=parseTrackerDate(v);
  if(!d)return esc(v||"");
  return String(d.getDate()).padStart(2,"0")+"-"+d.toLocaleDateString("en-US",{month:"short"})+"-"+d.getFullYear();
}

/* V161 reporting-month rule:
   Rahavan salary received on the last day or the day before month-end
   belongs to NEXT MONTH for reports/graphs only. The real transaction date,
   bank balance and Google Sheet row are not changed. */
function moneyReportingDate(x){
  const d=parseTrackerDate(x&&x.date);
  if(!d)return null;
  const sub=String((x&&x.subCategory)||"").trim().toLowerCase().replace(/\s+/g," ");
  const flow=typeof cashFlowBucketForEntry==="function"?cashFlowBucketForEntry(x):String((x&&x.mainCategory)||"").trim();
  if(flow==="Income" && sub==="rahavan salary"){
    const lastDay=new Date(d.getFullYear(),d.getMonth()+1,0).getDate();
    if(d.getDate()>=lastDay-1){
      return new Date(d.getFullYear(),d.getMonth()+1,1);
    }
  }
  return new Date(d.getFullYear(),d.getMonth(),d.getDate());
}

function categoryTotalsDisplayGroup(x){
  const flow=cashFlowBucketForEntry(x);

  if(flow==="Income")return "Income";
  if(flow==="Needs")return "Needs";
  if(flow==="Wants")return "Wants";
  if(flow==="Savings")return "Savings";
  if(flow==="Savings Return")return "Savings Return";
  if(flow==="In")return "In";
  if(flow==="Out")return "Out";
  if(flow==="Loan In")return "Loan In";
  if(flow==="Loan Out")return "Loan Out";
  return "Others";
}

/* ---------------- OPTION 1: Overall Transactions ---------------- */
let overallTransactionPeriod = "all";
let currentOverallTransactionData = [];
let option1PopupMain = "";
let option1PopupSub = "";

function openViewMode1(){
  document.getElementById("viewModeChooser").style.display="none";
  document.getElementById("viewModeContent").innerHTML=
    '<button class="secondary" onclick="backToViewOptions()">← Back</button>'+
    '<div class="view-section-title">'+
      '<h2>🧮 Overall Transactions</h2>'+
      '<p class="muted">Cumulative totals for every main category and sub category.</p>'+
    '</div>'+
    '<div class="period-tabs overall-period-tabs">'+
      '<button class="period-tab active" onclick="selectOverallTransactionPeriod(\'all\',this)">Overall</button>'+
      '<button class="period-tab" onclick="selectOverallTransactionPeriod(\'yearly\',this)">Yearly</button>'+
      '<button class="period-tab" onclick="selectOverallTransactionPeriod(\'monthly\',this)">Monthly</button>'+
      '<button class="period-tab" onclick="selectOverallTransactionPeriod(\'weekly\',this)">Weekly</button>'+
      '<button class="period-tab" onclick="selectOverallTransactionPeriod(\'daily\',this)">Daily</button>'+
    '</div>'+
    '<div id="overallTransactionControls"></div>'+
    '<div id="overallTransactionArea"></div>';

  selectOverallTransactionPeriod("all",document.querySelector("#viewModeContent .period-tab"));
}

function selectOverallTransactionPeriod(type,btn){
  overallTransactionPeriod=type;
  document.querySelectorAll("#viewModeContent .period-tab").forEach(function(x){x.classList.remove("active");});
  if(btn)btn.classList.add("active");

  const box=document.getElementById("overallTransactionControls");
  const now=new Date();

  if(type==="all"){
    box.innerHTML="";
    renderOverallTransactions(moneyEntries(),"Overall — All Transactions");
    return;
  }

  if(type==="yearly"){
    box.innerHTML=
      '<div class="card compact-period-control">'+
        '<label>Year<input id="overallYear" type="number" min="2000" max="2100" value="'+now.getFullYear()+'"></label>'+
        '<button class="primary" onclick="runOverallTransactions()">Show</button>'+
      '</div>';
  }else if(type==="monthly"){
    box.innerHTML=
      '<div class="card compact-period-control">'+
        '<label>Month<input id="overallMonth" type="month" value="'+now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,"0")+'"></label>'+
        '<button class="primary" onclick="runOverallTransactions()">Show</button>'+
      '</div>';
  }else if(type==="weekly"){
    const today=localDateValue(now);
    box.innerHTML=
      '<div class="card compact-period-control">'+
        '<label>Start Date<input id="overallWeekStart" type="date" value="'+today+'"></label>'+
        '<label>End Date<input id="overallWeekEnd" type="date" value="'+today+'"></label>'+
        '<button class="primary" onclick="runOverallTransactions()">Show</button>'+
      '</div>';
  }else{
    box.innerHTML=
      '<div class="card compact-period-control">'+
        '<label>Date<input id="overallDay" type="date" value="'+localDateValue(now)+'"></label>'+
        '<button class="primary" onclick="runOverallTransactions()">Show</button>'+
      '</div>';
  }

  runOverallTransactions();
}

function runOverallTransactions(){
  try{
  const type=overallTransactionPeriod;
  let data=moneyEntries();
  let title="Overall — All Transactions";

  if(type==="yearly"){
    const y=Number(document.getElementById("overallYear")?.value);
    data=data.filter(function(x){
      const d=moneyReportingDate(x);
      return d && d.getFullYear()===y;
    });
    title="Year "+y;
  }else if(type==="monthly"){
    const value=document.getElementById("overallMonth")?.value||"";
    if(!value)return;
    const parts=value.split("-"),y=Number(parts[0]),m=Number(parts[1])-1;
    data=data.filter(function(x){
      const d=moneyReportingDate(x);
      return d && d.getFullYear()===y && d.getMonth()===m;
    });
    title=new Date(y,m,1).toLocaleDateString("en-US",{month:"long",year:"numeric"});
  }else if(type==="weekly"){
    const sv=document.getElementById("overallWeekStart")?.value;
    const ev=document.getElementById("overallWeekEnd")?.value;
    if(!sv||!ev)return;
    const start=new Date(sv+"T00:00:00"),end=new Date(ev+"T23:59:59");
    data=data.filter(function(x){
      const d=moneyReportingDate(x);
      return d && d>=start && d<=end;
    });
    title=sv+" to "+ev;
  }else if(type==="daily"){
    const value=document.getElementById("overallDay")?.value;
    if(!value)return;
    const target=new Date(value+"T00:00:00");
    data=data.filter(function(x){
      const d=moneyReportingDate(x);
      return d &&
        d.getFullYear()===target.getFullYear() &&
        d.getMonth()===target.getMonth() &&
        d.getDate()===target.getDate();
    });
    title=value;
  }

  renderOverallTransactions(data,title);
  }catch(err){
    console.error("Overall Transactions error:",err);
    const area=document.getElementById("overallTransactionArea");
    if(area){
      area.innerHTML='<div class="card" style="border:1px solid #fecaca;background:#fef2f2;color:#991b1b">'+
        '<b>Could not build Overall Transactions</b><br><span>'+esc(err.message||String(err))+'</span></div>';
    }
  }
}

function renderOverallTransactions(data,title){
  currentOverallTransactionData = Array.isArray(data) ? data.slice() : [];
  const area=document.getElementById("overallTransactionArea");
  if(!area)return;

  if(!data.length){
    area.innerHTML='<div class="card"><p class="muted">No transactions found for '+esc(title)+'.</p></div>';
    return;
  }

  const order=["Income","Needs","Wants","Savings","In","Out","Loan In","Loan Out","Others"];
  const grouped={};

  data.forEach(function(x){
    const main=categoryTotalsDisplayGroup(x);
    const sub=String(x.subCategory||"Uncategorized").trim()||"Uncategorized";
    const amount=amountNumber(x.amount);

    if(!grouped[main])grouped[main]={total:0,count:0,subs:{}};
    grouped[main].total+=amount;
    grouped[main].count+=1;

    if(!grouped[main].subs[sub])grouped[main].subs[sub]={amount:0,count:0};
    grouped[main].subs[sub].amount+=amount;
    grouped[main].subs[sub].count+=1;
  });

  const periodFlow=moneyFlowTotals(data);
  const periodEnd=moneyMaxDate(data);
  const overallEndDate=moneyMaxDate(data);
  const totalCash=overallEndDate ? moneyCumulativeBalanceAt(overallEndDate) : moneyLatestCumulativeBalance();

  const mainCards=order.filter(function(main){return grouped[main];}).map(function(main){
    const g=grouped[main];
    return '<button class="overall-main-total '+overallMainClass(main)+' option1-clickable-card" '+
      'onclick="openOption1Transactions(\''+esc(main).replace(/'/g,"&#39;")+'\',\'\')">'+
      '<b>'+esc(main)+'</b>'+
      '<strong>'+moneyFmt(g.total)+'</strong>'+
      '<span>'+g.count+' transactions</span>'+
    '</button>';
  }).join('');

  const detailCards=order.filter(function(main){return grouped[main];}).map(function(main){
    const g=grouped[main];
    const rows=Object.entries(g.subs).sort(function(a,b){return b[1].amount-a[1].amount;});

    return '<div class="overall-category-card '+overallMainClass(main)+'">'+
      '<div class="overall-category-head">'+
        '<h3>'+esc(main)+'</h3>'+
        '<b>'+moneyFmt(g.total)+'</b>'+
      '</div>'+
      '<table class="overall-sub-table">'+
        '<thead><tr><th>Sub Category</th><th>Total</th><th>Txn</th></tr></thead>'+
        '<tbody>'+
          rows.map(function(row){
            return '<tr class="option1-sub-click-row" '+
              'onclick="openOption1Transactions(\''+esc(main).replace(/'/g,"&#39;")+'\',\''+esc(row[0]).replace(/'/g,"&#39;")+'\')">'+
              '<td><b>'+esc(row[0])+'</b></td>'+
              '<td>'+moneyFmt(row[1].amount)+'</td>'+
              '<td>'+row[1].count+'</td>'+
            '</tr>';
          }).join('')+
        '</tbody>'+
      '</table>'+
    '</div>';
  }).join('');

  // Meaningful money summary:
  // Income = earned/received income + Loan In.
  // Expenses = Needs + Wants + Loan Out.
  // Savings = Savings - Savings Return.
  // Transfer In / Transfer Out are intentionally excluded because they only move
  // money between the user's own accounts.
  const incomeTotal=(grouped.Income?.total||0)+(grouped["Loan In"]?.total||0);
  const needsTotal=(grouped.Needs?.total||0);
  const wantsTotal=(grouped.Wants?.total||0);
  const loanOutTotal=(grouped["Loan Out"]?.total||0);
  const expenseTotal=needsTotal+wantsTotal+loanOutTotal;
  const savingTotal=(grouped.Savings?.total||0);
  const savingsReturnTotal=data.reduce(function(sum,x){
    return cashFlowBucketForEntry(x)==="Savings Return" ? sum+amountNumber(x.amount) : sum;
  },0);
  const netSavings=savingTotal-savingsReturnTotal;

  const remaining=totalCash;
  const summaryTable=
    '<div class="card option1-overall-summary">'+
      '<h3>'+esc(title)+'</h3>'+
      '<table class="option1-summary-table">'+
        '<thead><tr><th>Money Summary</th><th>Amount</th><th>Meaning</th></tr></thead>'+
        '<tbody>'+
          '<tr><td><b>Income</b></td><td class="money-positive"><b>'+moneyFmt(incomeTotal)+'</b></td><td>Income + Loan In. Transfer In is excluded.</td></tr>'+
          '<tr><td><b>Expenses</b></td><td class="money-negative"><b>'+moneyFmt(expenseTotal)+'</b></td><td>Needs + Wants + Loan Out. Transfer Out is excluded.</td></tr>'+
          '<tr><td><b>Savings</b></td><td class="money-saving"><b>'+moneyFmt(netSavings)+'</b></td><td>Savings minus Savings Return</td></tr>'+
          '<tr class="option1-remaining-row"><td><b>Overall Remaining</b></td><td><b>'+moneyFmt(remaining)+'</b></td><td><b>Cumulative balance up to the end of this period</b></td></tr>'+
        '</tbody>'+
      '</table>'+
    '</div>';

  const txRows=data.slice().sort(function(a,b){
    const da=parseTrackerDate(a.date),db=parseTrackerDate(b.date);
    return (db?db.getTime():0)-(da?da.getTime():0);
  });

  const transactionTable=
    '<div class="card option1-transaction-card">'+
      '<h3>Transactions — '+txRows.length+'</h3>'+
      '<div class="option1-transaction-wrap">'+
        '<table class="option1-transaction-table">'+
          '<thead><tr>'+
            '<th>Date</th><th>Main Category</th><th>Sub Category</th><th>Explanation</th><th>Amount</th><th>Account</th>'+
          '</tr></thead>'+
          '<tbody>'+
            txRows.map(function(x){
              return '<tr>'+
                '<td>'+displayTrackerDate(x.date)+'</td>'+
                '<td style="text-align:center">'+esc(x.mainCategory||"")+'</td>'+
                '<td style="text-align:center">'+esc(x.subCategory||"")+'</td>'+
                '<td style="text-align:center">'+esc(x.explanation||"")+'</td>'+
                '<td>'+moneyFmt(x.amount)+'</td>'+
                '<td>'+esc(x.account||x.fromAccount||"")+'</td>'+
              '</tr>';
            }).join('')+
          '</tbody>'+
        '</table>'+
      '</div>'+
    '</div>';

  area.innerHTML=
    '<div class="overall-report-heading">'+
      '<div><h3>'+esc(title)+'</h3><span class="muted">'+data.length+' transactions</span></div>'+
      '<div><b>Overall Remaining:</b> <span class="'+(totalCash>=0?'money-positive':'money-negative')+'">'+moneyFmt(totalCash)+'</span></div>'+
    '</div>'+
    summaryTable+
    '<div class="overall-main-grid">'+mainCards+'</div>'+
    '<div class="overall-detail-grid">'+detailCards+'</div>'+
    transactionTable;
}


function option1EntryMatchesMain(x,main){
  const displayMain=categoryTotalsDisplayGroup(x);

  if(main==="Expenses"){
    return displayMain==="Needs" || displayMain==="Wants";
  }

  return displayMain===main;
}

function openOption1Transactions(main,sub){
  option1PopupMain=main||"";
  option1PopupSub=sub||"";

  const search=document.getElementById("option1PopupSearch");
  if(search)search.value="";

  const win=document.getElementById("option1TransactionPopup");
  if(win)win.style.display="flex";

  renderOption1TransactionPopup();
}

function closeOption1TransactionPopup(){
  const win=document.getElementById("option1TransactionPopup");
  if(win)win.style.display="none";
}

function renderOption1TransactionPopup(){
  const title=document.getElementById("option1PopupTitle");
  const summary=document.getElementById("option1PopupSummary");
  const box=document.getElementById("option1PopupTable");
  if(!box)return;

  const q=String(document.getElementById("option1PopupSearch")?.value||"")
    .trim()
    .toLowerCase();

  let data=(currentOverallTransactionData||[]).filter(function(x){
    if(!option1EntryMatchesMain(x,option1PopupMain))return false;

    if(option1PopupSub){
      const sub=String(x.subCategory||"Uncategorized").trim()||"Uncategorized";
      if(sub!==option1PopupSub)return false;
    }

    return true;
  });

  if(q){
    data=data.filter(function(x){
      return [
        x.date,x.day,x.mainCategory,x.subCategory,
        x.explanation,x.account,x.fromAccount
      ].some(function(v){
        return String(v||"").toLowerCase().includes(q);
      });
    });
  }

  data.sort(function(a,b){
    const da=parseTrackerDate(a.date),db=parseTrackerDate(b.date);
    return (db?db.getTime():0)-(da?da.getTime():0);
  });

  const total=data.reduce(function(sum,x){
    return sum+amountNumber(x.amount);
  },0);

  if(title){
    title.textContent =
      option1PopupSub
        ? option1PopupMain+" → "+option1PopupSub
        : option1PopupMain+" Transactions";
  }

  if(summary){
    summary.innerHTML=
      '<b>'+data.length+' transactions</b> &nbsp; • &nbsp; Total: <b>'+moneyFmt(total)+'</b>';
  }

  if(!data.length){
    box.innerHTML='<div class="card"><p class="muted">No matching transactions found.</p></div>';
    return;
  }

  box.innerHTML=
    '<div class="option1-popup-table-wrap">'+
      '<table class="option1-popup-table">'+
        '<thead><tr>'+
          '<th>Date</th>'+
          '<th>Day</th>'+
          '<th>Main Category</th>'+
          '<th>Sub Category</th>'+
          '<th>Explanation</th>'+
          '<th>Amount</th>'+
          '<th>Account</th>'+
        '</tr></thead>'+
        '<tbody>'+
          data.map(function(x){
            return '<tr>'+
              '<td>'+displayTrackerDate(x.date)+'</td>'+
              '<td style="text-align:center">'+esc(x.day||"")+'</td>'+
              '<td>'+esc(x.mainCategory||"")+'</td>'+
              '<td><b>'+esc(x.subCategory||"")+'</b></td>'+
              '<td>'+esc(x.explanation||"")+'</td>'+
              '<td class="option1-popup-amount">'+moneyFmt(x.amount)+'</td>'+
              '<td>'+esc(x.account||x.fromAccount||"")+'</td>'+
            '</tr>';
          }).join('')+
        '</tbody>'+
      '</table>'+
    '</div>';
}

function overallMainClass(main){
  if(main==="Income"||main==="In")return "tone-green";
  if(main==="Needs"||main==="Wants"||main==="Out")return "tone-red";
  if(main==="Savings")return "tone-blue";
  if(main==="Loan In")return "tone-cyan";
  if(main==="Loan Out")return "tone-orange";
  return "tone-grey";
}

/* ---------------- OPTION 2: Passbook Transactions ---------------- */
function openViewMode2(){
  document.getElementById("viewModeChooser").style.display="none";
  document.getElementById("viewModeContent").innerHTML=
    '<button class="secondary" onclick="backToViewOptions()">← Back</button>'+
    '<div class="view-section-title"><h2>📒 Passbook Transactions</h2><p class="muted">Chronological cash-flow summary with running cumulative balance.</p></div>'+
    '<div class="period-tabs">'+
      '<button class="period-tab active" onclick="showSummaryView(\'daily\',this)">Daily</button>'+
      '<button class="period-tab" onclick="showSummaryView(\'monthly\',this)">Monthly</button>'+
      '<button class="period-tab" onclick="showSummaryView(\'yearly\',this)">Yearly</button>'+
    '</div>'+
    '<div id="summaryViewArea"></div>';

  showSummaryView("daily",document.querySelector("#viewModeContent .period-tab"));
}
function summaryBucket(){
  return {
    income:0,needs:0,wants:0,saving:0,savingsReturn:0,
    in:0,out:0,loanIn:0,loanOut:0,others:0
  };
}

function addToSummary(bucket,x){
  const amount=amountNumber(x.amount);
  const flow=cashFlowBucketForEntry(x);

  if(flow==="Income")bucket.income+=amount;
  else if(flow==="Needs")bucket.needs+=amount;
  else if(flow==="Wants")bucket.wants+=amount;
  else if(flow==="Savings")bucket.saving+=amount;
  else if(flow==="Savings Return")bucket.savingsReturn+=amount;
  else if(flow==="In")bucket.in+=amount;
  else if(flow==="Out")bucket.out+=amount;
  else if(flow==="Loan In")bucket.loanIn+=amount;
  else if(flow==="Loan Out")bucket.loanOut+=amount;
  else bucket.others+=amount;
}

function rowRemaining(r){
  return (r.income||0)+(r.in||0)+(r.loanIn||0)+(r.savingsReturn||0)
       -(r.needs||0)-(r.wants||0)-(r.saving||0)
       -(r.out||0)-(r.loanOut||0)-(r.others||0);
}

function showSummaryView(type,btn){
  try{
  document.querySelectorAll("#viewModeContent .period-tab").forEach(function(x){x.classList.remove("active");});
  if(btn)btn.classList.add("active");

  const groups={};

  moneyEntries().forEach(function(x){
    const d=moneyReportingDate(x);
    if(!d)return;

    let key="",label="",extra="";

    if(type==="daily"){
      key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
      label=String(d.getDate()).padStart(2,"0")+"-"+d.toLocaleDateString("en-US",{month:"short"})+"-"+String(d.getFullYear()).slice(-2);
      extra=d.toLocaleDateString("en-US",{weekday:"short"});
    }else if(type==="monthly"){
      key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0");
      label=d.toLocaleDateString("en-US",{month:"short",year:"numeric"});
    }else{
      key=String(d.getFullYear());
      label=key;
    }

    if(!groups[key])groups[key]={label:label,extra:extra,data:summaryBucket()};
    addToSummary(groups[key].data,x);
  });

  const rows=Object.keys(groups).sort().map(function(k){
    groups[k].key=k;
    return groups[k];
  });

  let running=0;
  rows.forEach(function(r){
    running+=rowRemaining(r.data);
    r.cumulativeRemaining=running;
  });

  renderSummaryTable(type,rows.slice().reverse());
  }catch(err){
    console.error("Passbook report error:",err);
    const area=document.getElementById("summaryViewArea");
    if(area){
      area.innerHTML='<div class="card" style="border:1px solid #fecaca;background:#fef2f2;color:#991b1b">'+
        '<b>Could not build Passbook report</b><br><span>'+esc(err.message||String(err))+'</span></div>';
    }
  }
}

function renderSummaryTable(type,rows){
  const area=document.getElementById("summaryViewArea");

  if(!rows.length){
    area.innerHTML='<div class="card"><p class="muted">No money data available.</p></div>';
    return;
  }

  const total=summaryBucket();

  rows.forEach(function(r){
    Object.keys(total).forEach(function(k){
      total[k]+=Number(r.data[k]||0);
    });
  });

  const expenses=total.needs+total.wants;
  const totalIn=total.income+total.in+total.loanIn+total.savingsReturn;
  const totalOut=expenses+total.saving+total.out+total.loanOut+total.others;
  const finalBalance=rows.length ? Number(rows[0].cumulativeRemaining||0) : moneyLatestCumulativeBalance();

  const top=
    '<div class="view-summary-grid">'+
      '<div class="view-summary income"><b>Total In</b><div class="amt">'+moneyFmt(totalIn)+'</div></div>'+
      '<div class="view-summary expense"><b>Total Out</b><div class="amt">'+moneyFmt(totalOut)+'</div></div>'+
      '<div class="view-summary saving"><b>Overall Remaining</b><div class="amt">'+moneyFmt(finalBalance)+'</div></div>'+
    '</div>';

  const first=type==="daily"?"Date":type==="monthly"?"Monthly":"Year";
  const dayHead=type==="daily"?'<th>Day</th>':'';

  const body=rows.map(function(r){
    const d=r.data;
    const cumulative=Number(r.cumulativeRemaining||0);

    return '<tr>'+
      '<td>'+esc(r.label)+'</td>'+
      (type==="daily"?'<td>'+esc(r.extra)+'</td>':'')+
      '<td class="money-positive">'+moneyFmt(d.income)+'</td>'+
      '<td class="money-negative">'+moneyFmt(d.needs+d.wants)+'</td>'+
      '<td class="money-saving">'+moneyFmt(d.saving)+'</td>'+
      '<td class="money-positive">'+moneyFmt(d.in)+'</td>'+
      '<td class="money-negative">'+moneyFmt(d.out)+'</td>'+
      '<td class="loan-in-amount">'+moneyFmt(d.loanIn)+'</td>'+
      '<td class="loan-out-amount">'+moneyFmt(d.loanOut)+'</td>'+
      '<td>'+moneyFmt(d.others)+'</td>'+
      '<td class="'+(cumulative>=0?'money-positive':'money-negative')+'">'+moneyFmt(cumulative)+'</td>'+
    '</tr>';
  }).join('');

  area.innerHTML=
    top+
    '<div class="card summary-table-card">'+
      '<div style="display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap">'+
        '<h3 style="margin:0">'+(type==="daily"?"Daily Summary":type==="monthly"?"Monthly Summary":"Yearly Summary")+'</h3>'+
        '<div><b>Cumulative Balance:</b> <span class="'+(finalBalance>=0?'money-positive':'money-negative')+'">'+moneyFmt(finalBalance)+'</span></div>'+
      '</div>'+
      '<div style="overflow-x:auto">'+
        '<table class="summary-table cashflow-summary-table" style="margin-top:14px"><thead><tr>'+
          '<th>'+first+'</th>'+dayHead+
          '<th>Income</th><th>Expenses</th><th>Saving</th>'+
          '<th>In</th><th>Out</th><th>Loan In</th><th>Loan Out</th><th>Others</th>'+
          '<th>Cumulative<br>Balance</th>'+
        '</tr></thead><tbody>'+body+'</tbody></table>'+
      '</div>'+
    '</div>';
}


/* ---------------- OPTION 4: BANK WISE ---------------- */
let activeBankWiseAccount="";

function bankAccountName(x){
  return String(x.account||x.fromAccount||"").trim();
}

function bankWiseAccounts(){
  const set=new Set();
  (config.accounts||[]).forEach(function(a){
    a=String(a||"").trim();
    if(a)set.add(a);
  });
  moneyEntries().forEach(function(x){
    const a=bankAccountName(x);
    if(a)set.add(a);
  });
  return Array.from(set).sort(function(a,b){return a.localeCompare(b,undefined,{sensitivity:"base"});});
}

function bufferCheckpointValue(x){
  // getRoomDataForWeb() returns Column H as `remaining`.
  // Other Money readers may expose the same value as `remainingAmount`.
  const raw = (x && x.remainingAmount !== undefined && x.remainingAmount !== "")
    ? x.remainingAmount
    : (x ? x.remaining : "");
  const n = Number(String(raw === null || raw === undefined ? "" : raw).replace(/,/g,"").trim());
  return Number.isFinite(n) ? n : NaN;
}

function isBufferEntry(x){
  return String(x.mainCategory||"").trim().toLowerCase()==="buffer";
}

function bankWiseChronological(account){
  return moneyEntries()
    .filter(function(x){
      return bankAccountName(x).toLowerCase()===String(account).toLowerCase();
    })
    .slice()
    .sort(function(a,b){
      const da=parseTrackerDate(a.date), db=parseTrackerDate(b.date);
      return (da?da.getTime():0)-(db?db.getTime():0);
    });
}

/*
  BUFFER RULE
  ----------
  A Buffer row is a fixed known balance for that account.
  Example: Buffer Remaining Amount = 200.

  After Buffer:
      200 + later cash effects

  Before Buffer:
      calculate backwards from 200 by reversing earlier cash effects.

  Buffer itself never counts as Income / Expense / Savings.
*/

function isBankStartCheckpoint(x){
  if(isBufferEntry(x)) return true;

  // Allows a normal account row to be used as the starting point.
  // Example: Wallet, Transfer In, Amount 512,
  // Explanation = "to the wallet having balance to tally".
  const note=String(x.explanation||"").trim().toLowerCase();
  return note.includes("balance to tally") ||
         note.includes("balance tally") ||
         note.includes("opening balance");
}

function bankStartValue(x){
  if(isBufferEntry(x)){
    const n=bufferCheckpointValue(x);
    return Number.isFinite(n) ? n : 0;
  }

  // For a "balance to tally" row, Amount itself is the known balance.
  const n=Number(String(x.amount||0).replace(/,/g,""));
  return Number.isFinite(n) ? Math.abs(n) : 0;
}


function bankTxKey(x){
  return [
    String(x.date||""),
    String(x.mainCategory||""),
    String(x.subCategory||""),
    String(x.explanation||""),
    String(x.amount||""),
    String(bankAccountName(x)||""),
    String(x.sheetRow||x.row||x.__rowNumber||"")
  ].join("¦").toLowerCase();
}

function bankWiseBalanceMap(account){
  const allRows=bankWiseChronological(account);
  const map=new Map();

  if(!allRows.length){
    return {rows:[],map:map,current:0,startIndex:-1};
  }

  // Find the latest checkpoint belonging ONLY to the selected account.
  let startIndex=-1;
  for(let i=0;i<allRows.length;i++){
    if(isBankStartCheckpoint(allRows[i])) startIndex=i;
  }

  // If this account has no checkpoint yet, retain old calculation.
  if(startIndex<0){
    let running=0;
    allRows.forEach(function(x){
      running+=cashEffectForEntry(x);
      map.set(x,running); map.set(bankTxKey(x),running);
    });

    return {
      rows:allRows,
      map:map,
      current:running,
      startIndex:-1
    };
  }

  // Ignore all older rows before this account's starting point.
  const rows=allRows.slice(startIndex);

  // First row IS the known starting balance.
  let running=bankStartValue(rows[0]);
  map.set(rows[0],running); map.set(bankTxKey(rows[0]),running);

  // Calculate only later transactions for this same account.
  for(let i=1;i<rows.length;i++){
    const x=rows[i];

    // A newer checkpoint resets the balance again.
    if(isBankStartCheckpoint(x)){
      running=bankStartValue(x);
    }else{
      running+=cashEffectForEntry(x);
    }

    map.set(x,running); map.set(bankTxKey(x),running);
  }

  return {
    rows:rows,
    map:map,
    current:running,
    startIndex:startIndex,
    anchorBalance:bankStartValue(rows[0])
  };
}

function bankWiseCashBalance(account){
  const rows=moneyEntries().filter(function(x){
    return bankAccountName(x).toLowerCase()===String(account||"").toLowerCase();
  }).sort(function(a,b){
    const da=parseTrackerDate(a.date), db=parseTrackerDate(b.date);
    const ta=da?da.getTime():0, tb=db?db.getTime():0;
    if(tb!==ta)return tb-ta;
    const oa=Number(a.order||0), ob=Number(b.order||0);
    if(ob!==oa)return ob-oa;
    return Number(b.sheetRow||0)-Number(a.sheetRow||0);
  });

  for(let i=0;i<rows.length;i++){
    const n=sheetMoneyNumber(rows[i].remainingAmountRaw);
    if(n!==null) return n;
  }
  return 0;
}

function bankWiseSavingsGroups(account){
  const groups={};
  moneyEntries().forEach(function(x){
    if(bankAccountName(x).toLowerCase()!==String(account).toLowerCase())return;
    const flow=cashFlowBucketForEntry(x);
    if(flow!=="Savings" && flow!=="Savings Return")return;
    const sub=savingsBaseSubCategory(x) || "Savings";
    groups[sub]=(groups[sub]||0)+savingsSignedAmount(x);
  });
  return groups;
}

function bankWiseActiveSavings(account){
  const groups=bankWiseSavingsGroups(account);
  return Object.keys(groups).reduce(function(sum,k){return sum+Number(groups[k]||0);},0);
}

function bankWiseTransactions(account){
  const info=bankWiseBalanceMap(account);

  return info.rows.slice().sort(function(a,b){
    const da=parseTrackerDate(a.date), db=parseTrackerDate(b.date);
    const ta=da?da.getTime():0, tb=db?db.getTime():0;
    if(tb!==ta)return tb-ta;

    const oa=Number(a.order||0), ob=Number(b.order||0);
    if(ob!==oa)return ob-oa;

    const ra=Number(a.sheetRow||a.row||a.__rowNumber||0);
    const rb=Number(b.sheetRow||b.row||b.__rowNumber||0);
    return rb-ra;
  });
}

function openViewMode4(){
  document.getElementById("viewModeChooser").style.display="none";
  document.getElementById("viewModeContent").innerHTML=
    '<button class="secondary" onclick="backToViewOptions()">← Back</button>'+
    '<div class="view-section-title">'+
      '<h2>🏦 Bank Wise</h2>'+
      '<p class="muted">Cross-check every account with its cash balance, active savings and transaction history.</p>'+
    '</div>'+
    '<div id="bankWiseArea"></div>';
  activeBankWiseAccount="";
  renderBankWiseView();
}

function selectBankWiseAccount(account){
  activeBankWiseAccount=account;
  renderBankWiseView();
}


function bankSubCategoryMap(){
  const map={};
  const explicit=(config && config.subCategoryMainMap) || {};

  Object.keys(explicit).forEach(function(sub){
    const key=String(sub||"").trim().toLowerCase();
    if(key) map[key]=String(explicit[sub]||"").trim();
  });

  // Fallback only.
  Object.keys((config&&config.categories)||{}).forEach(function(main){
    ((config.categories&&config.categories[main])||[]).forEach(function(sub){
      const key=String(sub||"").trim().toLowerCase();
      if(key && !map[key]) map[key]=main;
    });
  });

  map["transfer in"]="In";
  map["transfer out"]="Out";
  return map;
}

function bankAllSubCategories(){
  const explicit=(config && config.subCategoryMainMap) || {};
  const allowedMains=new Set([
    "income","needs","wants","savings","in",
    "out","others","loan in","loan out","savings return"
  ]);

  const out=[];
  const seen=new Set();

  Object.keys(explicit).forEach(function(sub){
    const s=String(sub||"").trim();
    const main=String(explicit[sub]||"").trim().toLowerCase();
    const key=s.toLowerCase();
    if(s && allowedMains.has(main) && !seen.has(key)){
      seen.add(key);
      out.push(s);
    }
  });

  return out.sort(function(a,b){
    return a.localeCompare(b,undefined,{sensitivity:"base"});
  });
}

function bankMainForSub(sub){
  const key=String(sub||"").trim().toLowerCase();

  // Immediate authoritative mapping from the current Help sheet structure.
  // This prevents any old localStorage/category cache from filling the wrong Main Category.
  const fixed={
    "rahavan salary":"Income",
    "priyanka salary":"Income",
    "dividend":"Income",
    "interest - f/d":"Income",
    "coins":"Income",
    "bank mini balance interest":"Income",

    "rent":"Needs",
    "service":"Needs",
    "medical":"Needs",
    "groceries":"Needs",
    "zepto":"Needs",
    "recharge":"Needs",
    "petrol":"Needs",
    "travel":"Needs",
    "money lent":"Needs",
    "milk":"Needs",
    "veg":"Needs",
    "current bill":"Needs",
    "gas":"Needs",
    "egg":"Needs",
    "water":"Needs",
    "pooja":"Needs",
    "oil":"Needs",
    "atm":"Needs",
    "don't know":"Needs",
    "things":"Needs",
    "non-veg":"Needs",
    "dress":"Needs",
    "fruits":"Needs",
    "hotel":"Needs",
    "movie":"Needs",
    "snacks":"Needs",
    "hair cutting":"Needs",
    "tea":"Needs",
    "curd":"Needs",

    "gold":"Savings",
    "f/d":"Savings",
    "ppf":"Savings",
    "stocks":"Savings",
    "zerodha":"Savings",
    "angel one":"Savings",

    "transfer in":"In",
    "transfer out":"Out",
    "priyanka actual salary":"Others",
    "loan received":"Loan In",
    "loan repayment received":"Loan In",
    "gifts i received":"Loan In",
    "loan i gave":"Loan Out",
    "loan repayment paid":"Loan Out",
    "gifts i gave":"Loan Out",
    "savings return":"Savings Return",
    "f/d maturity":"Savings Return",
    "ppf withdrawal":"Savings Return",
    "gold sale":"Savings Return",
    "stock withdrawal":"Savings Return"
  };

  if(fixed[key]) return fixed[key];

  // New categories added later in Help sheet still work through the live backend map.
  return bankSubCategoryMap()[key]||"";
}

function bankQuickEntryHtml(account){
  const subs=bankAllSubCategories();
  const today=new Date();
  const yyyy=today.getFullYear();
  const mm=String(today.getMonth()+1).padStart(2,"0");
  const dd=String(today.getDate()).padStart(2,"0");
  const dateValue=yyyy+"-"+mm+"-"+dd;

  return '<div class="bank-quick-entry">'+
    '<div class="bank-quick-entry-head">'+
      '<div><h3>✍️ Add Transaction — '+esc(account)+'</h3>'+
      '<div class="muted">Choose Sub Category first. Main Category is filled automatically.</div></div>'+
    '</div>'+
    '<div class="bank-quick-grid">'+
      '<label>Date<input id="bwDate" type="date" value="'+dateValue+'"></label>'+
      '<label>Sub Category<select id="bwSub" onchange="updateBankQuickMainFromSub()">'+
        '<option value="">Choose Sub Category</option>'+
        subs.map(function(s){return '<option value="'+esc(s)+'">'+esc(s)+'</option>';}).join("")+
      '</select></label>'+
      '<label>Main Category<input id="bwMain" value="" placeholder="Auto-filled" readonly></label>'+
      '<label>Amount<input id="bwAmount" type="number" step="0.01" placeholder="0.00"></label>'+
    '</div>'+
    '<div class="bank-quick-line">'+
      '<label>Explanation<input id="bwExplanation" placeholder="What was this transaction for?"></label>'+
      '<label>Account<input value="'+esc(account)+'" disabled><input id="bwAccount" type="hidden" value="'+esc(account)+'"></label>'+
      '<button class="primary" id="bwSaveBtn" onclick="saveBankWiseEntry()">💾 Save & Sync</button>'+
    '</div>'+
    '<div id="bwSaveStatus" class="muted" style="margin-top:8px"></div>'+
  '</div>';
}

function updateBankQuickMainFromSub(){
  const sub=document.getElementById("bwSub");
  const main=document.getElementById("bwMain");
  if(!sub||!main)return;
  main.value=bankMainForSub(sub.value);
}

async function saveBankWiseEntry(){
  const entry={
    date:(document.getElementById("bwDate")||{}).value||"",
    mainCategory:bankMainForSub((document.getElementById("bwSub")||{}).value||""),
    subCategory:(document.getElementById("bwSub")||{}).value||"",
    explanation:(document.getElementById("bwExplanation")||{}).value||"",
    amount:Number(((document.getElementById("bwAmount")||{}).value)||0),
    account:(document.getElementById("bwAccount")||{}).value||activeBankWiseAccount,
    fromAccount:(document.getElementById("bwAccount")||{}).value||activeBankWiseAccount,
    toAccount:""
  };

  if(!entry.date||!entry.mainCategory||!entry.subCategory||!entry.amount||!entry.account){
    alert("Please enter Date, Amount and Sub Category. Main Category will be filled automatically.");
    return;
  }

  const btn=document.getElementById("bwSaveBtn");
  const status=document.getElementById("bwSaveStatus");
  if(btn){btn.disabled=true;btn.textContent="Saving…";}

  if(status)status.textContent="Saving to Google Sheet…";
  setGoogleSyncStatus("Saving transaction to Google Sheet…",null);

  try{
    const result=await addTransactionToGoogleSheet(entry);

    // Sheet is the master. Re-read it immediately after the confirmed save.
    setGoogleSyncStatus("Google Sheet saved ✓ · updating website…",true);
    await syncFromGoogleSheet(false);

    if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
    if(typeof RV_renderAll==="function")RV_renderAll();
    renderBankWiseView();

    const successStatus=document.getElementById("bwSaveStatus");
    if(successStatus)successStatus.textContent="Saved & synced ✓";
    setGoogleSyncStatus("Saved & synced ✓",true);

  }catch(err){
    console.error(err);

    if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
    if(typeof RV_renderAll==="function")RV_renderAll();
    renderBankWiseView();

    setGoogleSyncStatus("Google save failed.",false);
    alert("Could not save transaction.\n"+((err&&err.message)||err));
  }
}

function renderBankWiseView(){
  const host=document.getElementById("bankWiseArea");
  if(!host)return;

  const accounts=bankWiseAccounts();
  if(!accounts.length){
    host.innerHTML='<div class="note">No bank/account names found yet. Add accounts in Money → Others → Set.</div>';
    return;
  }

  if(!activeBankWiseAccount || !accounts.some(function(a){return a===activeBankWiseAccount;})){
    activeBankWiseAccount=accounts[0];
  }

  const overallCash=accounts.reduce(function(s,a){return s+bankWiseCashBalance(a);},0);
  const overallSavings=accounts.reduce(function(s,a){return s+bankWiseActiveSavings(a);},0);

  let html=
    '<div class="bank-wise-summary">'+
      '<div class="bank-wise-kpi"><span>Total Cash Balance</span><b>'+moneyFmt(overallCash)+'</b></div>'+
      '<div class="bank-wise-kpi"><span>Total Active Savings</span><b>'+moneyFmt(overallSavings)+'</b></div>'+
      '<div class="bank-wise-kpi"><span>Total Position</span><b>'+moneyFmt(overallCash+overallSavings)+'</b></div>'+
      '<div class="bank-wise-kpi"><span>Accounts</span><b>'+accounts.length+'</b></div>'+
    '</div>'+
    '<h3>Accounts</h3>'+
    '<div class="bank-account-grid">'+
      accounts.map(function(a){
        const cash=bankWiseCashBalance(a);
        const sav=bankWiseActiveSavings(a);
        const tx=bankWiseTransactions(a).length;
        return '<button class="bank-account-card '+(a===activeBankWiseAccount?'active':'')+'" onclick="selectBankWiseAccount(\''+esc(a).replace(/'/g,"\\'")+'\')">'+
          '<b>🏦 '+esc(a)+'</b>'+
          '<span>Cash: '+moneyFmt(cash)+'</span>'+
          '<span>Savings: '+moneyFmt(sav)+' · '+tx+' txns</span>'+
        '</button>';
      }).join("")+
    '</div>';

  const account=activeBankWiseAccount;
  const cash=bankWiseCashBalance(account);
  const groups=bankWiseSavingsGroups(account);
  const activeSavings=bankWiseActiveSavings(account);
  const txs=bankWiseTransactions(account);

  html+=
    '<div class="card">'+
      '<h2 style="margin-top:0">🏦 '+esc(account)+'</h2>'+
      bankQuickEntryHtml(account)+
      '<div class="bank-wise-summary">'+
        '<div class="bank-wise-kpi"><span>Remaining / Cash</span><b>'+moneyFmt(cash)+'</b></div>'+
        '<div class="bank-wise-kpi"><span>Active Savings</span><b>'+moneyFmt(activeSavings)+'</b></div>'+
        '<div class="bank-wise-kpi"><span>Total Position</span><b>'+moneyFmt(cash+activeSavings)+'</b></div>'+
        '<div class="bank-wise-kpi"><span>Transactions</span><b>'+txs.length+'</b></div>'+
      '</div>'+
      '<h3>Active Savings in this account</h3>';

  const savingKeys=Object.keys(groups).sort(function(a,b){return groups[b]-groups[a];});
  if(savingKeys.length){
    html+='<div>'+
      savingKeys.map(function(k){
        return '<span class="bank-saving-chip">'+esc(k)+' · '+moneyFmt(groups[k])+'</span>';
      }).join("")+
    '</div>';
  }else{
    html+='<p class="muted">No active savings recorded for this account.</p>';
  }

  html+='<div class="room-split-note" style="margin-top:14px"><b>Balance source:</b> Account Remaining is read directly from Google Sheet column H and Overall Remaining directly from column I.</div>'+
    '<h3 style="margin-top:18px">Transactions <span class="muted" style="font-size:11px;font-weight:400">· newest first</span></h3>'+
    '<div class="muted" style="font-size:11px;margin:-6px 0 8px"><span style="color:#15803d;font-weight:800">Green = money in</span> · <span style="color:#dc2626;font-weight:800">Red = money out</span> · Remaining Balance = account cash after that transaction</div>';

  if(txs.length){
    const rows=txs.map(function(x){
      const isBuf=isBufferEntry(x);
      const effect=cashEffectForEntry(x);
      const amountColor=isBuf ? "#7c3aed" : (effect>0 ? "#15803d" : (effect<0 ? "#dc2626" : "#475569"));
      const amountDisplay=isBuf
        ? "BUFFER"
        : ((effect>0 ? "+" : (effect<0 ? "−" : ""))+moneyFmt(Math.abs(Number(x.amount||0))));

      // Google Sheet is now the source of truth:
      // B = Day, H = Account Remaining, I = Overall Remaining, J = Order.
      const accountRemaining=sheetMoneyNumber(x.remainingAmountRaw);
      const overallRemaining=sheetMoneyNumber(x.overallRemainingRaw);

      return '<tr'+(isBuf?' style="background:#f5f3ff"':'')+'>'+
        '<td style="text-align:center">'+esc(displayTrackerDate(x.date))+'</td>'+
        '<td>'+esc(x.day||"")+'</td>'+
        '<td>'+esc(x.mainCategory||"")+'</td>'+
        '<td>'+esc(x.subCategory||"")+'</td>'+
        '<td>'+esc(x.explanation||"")+'</td>'+
        '<td style="text-align:center;font-weight:800;color:'+amountColor+'">'+amountDisplay+'</td>'+
        '<td style="text-align:center;font-weight:900">'+(accountRemaining===null?'—':moneyFmt(accountRemaining))+'</td>'+
        '<td style="text-align:center;font-weight:900">'+(overallRemaining===null?'—':moneyFmt(overallRemaining))+'</td>'+
      '</tr>';
    }).join("");

    html+='<div class="bank-tx-table"><table class="bank-centered-table"><thead><tr>'+
      '<th style="text-align:center">Date</th><th style="text-align:center">Day</th><th style="text-align:center">Main Category</th><th style="text-align:center">Sub Category</th><th style="text-align:center">Explanation</th><th style="text-align:center">Amount</th><th style="text-align:center">Account Remaining</th><th style="text-align:center">Overall Remaining</th>'+
      '</tr></thead><tbody>'+
      rows+
      '</tbody></table></div>';
  }else{
    html+='<p class="muted">No transactions found for this account.</p>';
  }

  html+='</div>';
  host.innerHTML=html;
}



/* ---------------- OPTION 5: ROOM — SHARING + GIFTS ---------------- */
let ROOM_people=[];
let ROOM_activePerson="";
let ROOM_rows=[];
let ROOM_mode="home";

function ROOM_splitNames(v){
  return String(v||"").split(",").map(function(x){return x.trim();}).filter(Boolean);
}
function ROOM_isGiftRow(x){
  const s=String(x.subCategory||"").trim().toLowerCase();
  return s==="gift i received" || s==="gift i sent";
}
function ROOM_isGiftReceived(x){
  return String(x.subCategory||"").trim().toLowerCase()==="gift i received";
}
function ROOM_isGiftSent(x){
  return String(x.subCategory||"").trim().toLowerCase()==="gift i sent";
}

/* -------- V157 Sharing logic: shared expense + Sharing In / Sharing Out --------
   Normal shared expense + Kapil:
     Rahavan + Kapil => Kapil owes 1/2 of the bill.
   Normal shared expense + Kapil,Naveen:
     Rahavan + 2 friends => each friend owes 1/3 of the bill.

   Sharing In + Kapil:
     Kapil paid money back to Rahavan => FULL amount reduces Kapil's balance. No division.

   Sharing Out + Kapil:
     Kapil paid the bill / Rahavan has to give money to Kapil => FULL amount makes Rahavan owe Kapil.
     No division.

   Gift I Received / Gift I Sent are excluded completely from Sharing.
*/
function ROOM_sharingType(x){
  const s=String(x.subCategory||"").trim().toLowerCase();
  if(s==="sharing in")return "in";
  if(s==="sharing out")return "out";
  return "expense";
}
function ROOM_isRepayment(x,person){
  if(ROOM_isGiftRow(x))return false;
  const names=ROOM_splitNames(x.sharing).map(function(n){return n.toLowerCase();});
  const p=String(person||"").trim().toLowerCase();
  if(names.indexOf(p)===-1)return false;
  return ROOM_sharingType(x)==="in";
}
function ROOM_isSharingOut(x,person){
  if(ROOM_isGiftRow(x))return false;
  const names=ROOM_splitNames(x.sharing).map(function(n){return n.toLowerCase();});
  const p=String(person||"").trim().toLowerCase();
  if(names.indexOf(p)===-1)return false;
  return ROOM_sharingType(x)==="out";
}
function ROOM_personEffect(x,person){
  if(ROOM_isGiftRow(x))return 0;

  const names=ROOM_splitNames(x.sharing);
  const lower=names.map(function(n){return n.toLowerCase();});
  const p=String(person||"").trim().toLowerCase();
  if(lower.indexOf(p)===-1)return 0;

  const amount=Number(x.amount||0);
  if(!amount)return 0;

  const type=ROOM_sharingType(x);

  // Sharing In = friend paid me. Full amount reduces what the friend owes me.
  if(type==="in")return -amount;

  // Sharing Out = the friend paid the bill / I need to give them this amount.
  // Full amount makes my balance toward that friend negative. No division.
  if(type==="out")return -amount;

  // Normal shared expense only: split between Rahavan + listed friends.
  // Ignore an accidentally typed "Rahavan" in the Sharing list when counting people.
  const friends=names.filter(function(n){return n.toLowerCase()!=="rahavan";});
  if(!friends.length)return 0;
  return amount/(friends.length+1);
}
function ROOM_personTransactions(person){
  return ROOM_rows.filter(function(x){
    if(ROOM_isGiftRow(x))return false;
    return ROOM_splitNames(x.sharing).some(function(n){
      return n.toLowerCase()===String(person).toLowerCase();
    });
  }).sort(function(a,b){
    const da=parseTrackerDate(a.date),db=parseTrackerDate(b.date);
    const ta=da?da.getTime():0,tb=db?db.getTime():0;
    if(ta!==tb)return tb-ta;
    return Number(b.rowNumber||0)-Number(a.rowNumber||0);
  });
}
function ROOM_personBalance(person){
  return ROOM_personTransactions(person).reduce(function(s,x){
    return s+ROOM_personEffect(x,person);
  },0);
}

/* -------- Gift ledger --------
   Gift I Received from Sam ₹1000 => +1000 => RED: I should give Sam ₹1000 someday.
   Gift I Sent to Sam ₹1000      => -1000 => tally to zero.
   If sent becomes greater than received => GREEN difference in my favour.
   This tracker never changes Money totals; the original Income/Expense transaction does that.
*/
function GIFT_personTransactions(person){
  return ROOM_rows.filter(function(x){
    if(!ROOM_isGiftRow(x))return false;
    return ROOM_splitNames(x.sharing).some(function(n){
      return n.toLowerCase()===String(person).toLowerCase();
    });
  }).sort(function(a,b){
    const da=parseTrackerDate(a.date),db=parseTrackerDate(b.date);
    const ta=da?da.getTime():0,tb=db?db.getTime():0;
    if(ta!==tb)return tb-ta;
    return Number(b.rowNumber||0)-Number(a.rowNumber||0);
  });
}
function GIFT_effect(x){
  const a=Number(x.amount||0);
  if(ROOM_isGiftReceived(x))return a;
  if(ROOM_isGiftSent(x))return -a;
  return 0;
}
function GIFT_personBalance(person){
  return GIFT_personTransactions(person).reduce(function(s,x){return s+GIFT_effect(x);},0);
}
function GIFT_status(person,balance){
  if(Math.abs(balance)<0.005)return {text:"Tallied",cls:"gift-zero"};
  if(balance>0)return {text:"I should give "+person+" "+moneyFmt(balance),cls:"gift-red"};
  return {text:"My gift is ahead by "+moneyFmt(Math.abs(balance)),cls:"gift-green"};
}

function ROOM_allPeopleFromTransactions(){
  const set=new Set(ROOM_people||[]);
  ROOM_rows.forEach(function(x){ROOM_splitNames(x.sharing).forEach(function(n){
    if(n && n.toLowerCase()!=="rahavan")set.add(n);
  });});
  return Array.from(set).sort(function(a,b){return a.localeCompare(b,undefined,{sensitivity:"base"});});
}
function ROOM_loadPeople(){
  return new Promise(function(resolve){
    if(!(window.google&&google.script&&google.script.run)){resolve([]);return;}
    google.script.run
      .withSuccessHandler(function(r){
        ROOM_people=(r&&r.success&&Array.isArray(r.people))?r.people:[];
        ROOM_rows=(r&&r.success&&Array.isArray(r.rows))?r.rows:[];
        const dl=document.getElementById("roomSharingPeopleList");
        if(dl)dl.innerHTML=ROOM_people.map(function(p){return '<option value="'+esc(p)+'"></option>';}).join("");
        resolve(ROOM_people);
      })
      .withFailureHandler(function(err){
        ROOM_people=[];ROOM_rows=[];
        const host=document.getElementById("roomArea");
        if(host)host.innerHTML='<div class="note">Room sync failed: '+esc((err&&err.message)||String(err))+'</div>';
        resolve([]);
      })
      .getRoomDataForWeb();
  });
}

async function openViewMode5(){
  document.getElementById("viewModeChooser").style.display="none";
  ROOM_mode="home";
  ROOM_activePerson="";
  document.getElementById("viewModeContent").innerHTML=
    '<button class="secondary" onclick="backToViewOptions()">← Back</button>'+
    '<div class="view-section-title"><h2>🏠 Room</h2>'+
    '<p class="muted">Choose Sharing, Gifts or your private family money ledger.</p></div>'+
    '<div id="roomArea"><div class="muted">Reading Room data directly from Google Sheet...</div></div>';
  await ROOM_loadPeople();
  ROOM_renderHome();
}
function ROOM_backHome(){ROOM_mode="home";ROOM_activePerson="";ROOM_renderHome();}
function ROOM_renderHome(){
  const host=document.getElementById("roomArea");if(!host)return;
  host.innerHTML=
    '<div class="room-mode-grid">'+
      '<button class="room-mode-card" onclick="ROOM_openSharing()">'+
        '<span class="ico">🤝</span><b>1. Sharing</b>'+
        '<span>Existing shared-expense calculation. Your current split and settlement logic stays unchanged.</span>'+
      '</button>'+
      '<button class="room-mode-card" onclick="ROOM_openGifts()">'+
        '<span class="ico">🎁</span><b>2. Gifts</b>'+
        '<span>Track Gift I Received and Gift I Sent person-wise. Received shows red until matched by gifts sent.</span>'+
      '</button>'+
      '<button class="room-mode-card" onclick="ROOM_openPrivateLedger()">'+
        '<span class="ico">🔐</span><b>3. Family Private Ledger</b>'+
        '<span>Priyanka holding + my private Angel One tally. Reads Money data, but nothing from here changes Money, Sharing or Gifts.</span>'+
      '</button>'+
    '</div>';
}
function ROOM_openSharing(){ROOM_mode="sharing";ROOM_activePerson="";ROOM_renderSharing();}
function ROOM_openGifts(){ROOM_mode="gifts";ROOM_activePerson="";ROOM_renderGifts();}
function ROOM_selectPerson(name){
  ROOM_activePerson=name;
  if(ROOM_mode==="gifts")ROOM_renderGifts();
  else ROOM_renderSharing();
}

/* -------- Sharing screen -------- */
function ROOM_renderSharing(){
  const host=document.getElementById("roomArea");if(!host)return;
  const people=ROOM_allPeopleFromTransactions().filter(function(p){return ROOM_personTransactions(p).length>0;});
  let head='<button class="secondary" onclick="ROOM_backHome()">← Room</button>'+
    '<div class="view-section-title"><h2>🤝 Sharing</h2><p class="muted">Shared expenses are divided. Sharing In / Sharing Out use the full amount. Gifts are excluded.</p></div>'+
    '<div class="room-split-note"><b>Shared expense:</b> ₹2,000 + Kapil = ₹1,000 due from Kapil; Kapil,Naveen = ₹666.67 each. <b>Sharing In:</b> full amount received from that person reduces their balance. <b>Sharing Out:</b> that person paid the bill, so the full amount becomes money I owe them. <b>No /2 for Sharing In/Out.</b></div>';
  if(!people.length){host.innerHTML=head+'<div class="note">No shared-expense transactions found.</div>';return;}
  if(!ROOM_activePerson||people.indexOf(ROOM_activePerson)===-1)ROOM_activePerson=people[0];

  const totalOwed=people.reduce(function(s,p){return s+Math.max(0,ROOM_personBalance(p));},0);
  const settled=people.filter(function(p){return Math.abs(ROOM_personBalance(p))<0.005;}).length;

  let h=head+'<div class="room-top">'+
    '<div class="room-kpi"><span>Total Friends Owe Me</span><b>'+moneyFmt(totalOwed)+'</b></div>'+
    '<div class="room-kpi"><span>People</span><b>'+people.length+'</b></div>'+
    '<div class="room-kpi"><span>Fully Settled</span><b>'+settled+'</b></div>'+
  '</div><h3>People</h3><div class="room-person-grid">';

  h+=people.map(function(p){
    const bal=ROOM_personBalance(p);
    const status=Math.abs(bal)<0.005?'Settled':(bal>0?p+' owes me '+moneyFmt(bal):'I owe '+p+' '+moneyFmt(Math.abs(bal)));
    return '<button class="room-person-card '+(p===ROOM_activePerson?'active':'')+'" onclick="ROOM_selectPerson(\''+esc(p).replace(/'/g,"\\'")+'\')">'+
      '<b>👤 '+esc(p)+'</b><span class="'+(Math.abs(bal)<0.005?'room-status-settled':'room-status-owe')+'">'+esc(status)+'</span></button>';
  }).join('')+'</div>';

  const p=ROOM_activePerson, tx=ROOM_personTransactions(p), bal=ROOM_personBalance(p);
  h+='<div class="card"><h2 style="margin-top:0">👤 Rahavan ↔ '+esc(p)+'</h2>'+
     '<div class="room-top">'+
       '<div class="room-kpi"><span>Current Status</span><b class="'+(Math.abs(bal)<0.005?'room-status-settled':'room-status-owe')+'">'+
         (Math.abs(bal)<0.005?'Settled':(bal>0?esc(p)+' owes me '+moneyFmt(bal):'I owe '+esc(p)+' '+moneyFmt(Math.abs(bal))))+
       '</b></div>'+
       '<div class="room-kpi"><span>Shared Entries</span><b>'+tx.length+'</b></div>'+
       '<div class="room-kpi"><span>Outstanding</span><b>'+moneyFmt(Math.abs(bal))+'</b></div>'+
     '</div>';

  if(tx.length){
    let running=0;
    const chronological=tx.slice().reverse();
    const runMap=new Map();
    chronological.forEach(function(x){running+=ROOM_personEffect(x,p);runMap.set(x,running);});
    h+='<div class="room-table"><table><thead><tr>'+
      '<th>Date</th><th>Reason</th><th>Total Bill</th><th>Sharing</th><th>'+esc(p)+' Share / Return</th><th>Balance</th>'+
      '</tr></thead><tbody>'+
      tx.map(function(x){
        const eff=ROOM_personEffect(x,p), repayment=ROOM_isRepayment(x,p), sharingOut=ROOM_isSharingOut(x,p);
        const rb=runMap.get(x)||0;
        const actionLabel=repayment?'Sharing In':(sharingOut?'Sharing Out · I owe':'Share');
        const sign=eff<0?'− ':'+ ';
        const actionColor=repayment?'#15803d':(sharingOut?'#2563eb':'#b45309');
        return '<tr><td>'+esc(displayTrackerDate(x.date))+'</td>'+
          '<td>'+esc(x.explanation||x.subCategory||"")+'</td>'+
          '<td>'+moneyFmt(x.amount)+'</td>'+
          '<td>'+esc(x.sharing||"")+'</td>'+
          '<td style="font-weight:800;color:'+actionColor+'">'+actionLabel+' '+sign+moneyFmt(Math.abs(eff))+'</td>'+
          '<td style="font-weight:800">'+moneyFmt(rb)+'</td></tr>';
      }).join('')+'</tbody></table></div>';
  }
  h+='</div>';
  host.innerHTML=h;
}

/* -------- Gifts screen -------- */
function ROOM_renderGifts(){
  const host=document.getElementById("roomArea");if(!host)return;
  const people=ROOM_allPeopleFromTransactions().filter(function(p){return GIFT_personTransactions(p).length>0;});
  let head='<button class="secondary" onclick="ROOM_backHome()">← Room</button>'+
    '<div class="view-section-title"><h2>🎁 Gifts</h2>'+
    '<p class="muted">Gift I Received = red amount I should return through a future gift. Gift I Sent reduces it. Every gift remains in history.</p></div>'+
    '<div class="room-split-note"><b>No sharing division here.</b> Sam + Gift I Received ₹1,000 = full ₹1,000 red. Later Gift I Sent ₹1,000 to Sam = Tallied ₹0.</div>';

  if(!people.length){
    host.innerHTML=head+'<div class="note">No gift transactions found yet. Use <b>Gift I Received</b> or <b>Gift I Sent</b> and select the person in Sharing.</div>';
    return;
  }
  if(!ROOM_activePerson||people.indexOf(ROOM_activePerson)===-1)ROOM_activePerson=people[0];

  const totalToGive=people.reduce(function(s,p){return s+Math.max(0,GIFT_personBalance(p));},0);
  const totalAhead=people.reduce(function(s,p){return s+Math.max(0,-GIFT_personBalance(p));},0);
  const tallied=people.filter(function(p){return Math.abs(GIFT_personBalance(p))<0.005;}).length;

  let h=head+'<div class="room-top">'+
    '<div class="room-kpi"><span>I Should Give</span><b class="gift-red">'+moneyFmt(totalToGive)+'</b></div>'+
    '<div class="room-kpi"><span>My Gifts Ahead</span><b class="gift-green">'+moneyFmt(totalAhead)+'</b></div>'+
    '<div class="room-kpi"><span>Tallied People</span><b>'+tallied+' / '+people.length+'</b></div>'+
  '</div><h3>People</h3><div class="room-person-grid">';

  h+=people.map(function(p){
    const bal=GIFT_personBalance(p), st=GIFT_status(p,bal);
    return '<button class="room-person-card '+(p===ROOM_activePerson?'active':'')+'" onclick="ROOM_selectPerson(\''+esc(p).replace(/'/g,"\\'")+'\')">'+
      '<b>🎁 '+esc(p)+'</b><span class="'+st.cls+'">'+esc(st.text)+'</span></button>';
  }).join('')+'</div>';

  const p=ROOM_activePerson,tx=GIFT_personTransactions(p),bal=GIFT_personBalance(p),st=GIFT_status(p,bal);
  const received=tx.reduce(function(s,x){return s+(ROOM_isGiftReceived(x)?Number(x.amount||0):0);},0);
  const sent=tx.reduce(function(s,x){return s+(ROOM_isGiftSent(x)?Number(x.amount||0):0);},0);

  h+='<div class="card"><h2 style="margin-top:0">🎁 Rahavan ↔ '+esc(p)+'</h2>'+
    '<div class="room-top">'+
      '<div class="room-kpi"><span>Gift Received</span><b>'+moneyFmt(received)+'</b></div>'+
      '<div class="room-kpi"><span>Gift Sent</span><b>'+moneyFmt(sent)+'</b></div>'+
      '<div class="room-kpi"><span>Current Gift Status</span><b class="'+st.cls+'">'+esc(st.text)+'</b></div>'+
    '</div>';

  let running=0;
  const chronological=tx.slice().reverse();
  const runMap=new Map();
  chronological.forEach(function(x){running+=GIFT_effect(x);runMap.set(x,running);});
  h+='<div class="room-table"><table><thead><tr>'+
    '<th>Date</th><th>Type</th><th>Reason</th><th>Amount</th><th>Person</th><th>Running Gift Balance</th>'+
    '</tr></thead><tbody>'+
    tx.map(function(x){
      const rb=runMap.get(x)||0;
      const cls=Math.abs(rb)<0.005?'gift-zero':(rb>0?'gift-red':'gift-green');
      return '<tr>'+
        '<td>'+esc(displayTrackerDate(x.date))+'</td>'+
        '<td><b>'+esc(x.subCategory||"")+'</b></td>'+
        '<td>'+esc(x.explanation||"")+'</td>'+
        '<td>'+moneyFmt(x.amount)+'</td>'+
        '<td>'+esc(x.sharing||"")+'</td>'+
        '<td class="'+cls+'">'+moneyFmt(Math.abs(rb))+(Math.abs(rb)<0.005?' · Tallied':(rb>0?' · I should give':' · My gift ahead'))+'</td>'+
      '</tr>';
    }).join('')+'</tbody></table></div></div>';
  host.innerHTML=h;
}


/* -------- V163 Room Option 3: Family Private Ledger -------- */
let PRIVATE_data=null, PRIVATE_tab="monthly", PRIVATE_monthKey="", PRIVATE_year="";
function ROOM_openPrivateLedger(){ROOM_mode="private";ROOM_activePerson="";PRIVATE_load();}
function PRIVATE_load(){
  const host=document.getElementById("roomArea"); if(!host)return;
  host.innerHTML='<button class="secondary" onclick="ROOM_backHome()">← Room</button><div class="view-section-title"><h2>🔐 Family Private Ledger</h2><p class="muted">Private read-only analysis of Money data. Settings entered here stay inside this ledger.</p></div><div class="muted">Reading private ledger...</div>';
  google.script.run.withSuccessHandler(function(d){
    if(!d||!d.success){host.innerHTML+='<div class="note">'+esc((d&&d.message)||"Unable to load")+'</div>';return;}
    PRIVATE_data=d; const now=new Date();
    if(!PRIVATE_monthKey)PRIVATE_monthKey=now.getFullYear()+"-"+String(now.getMonth()+1).padStart(2,"0");
    if(!PRIVATE_year)PRIVATE_year=String(now.getFullYear());
    PRIVATE_render();
  }).withFailureHandler(function(e){host.innerHTML+='<div class="note">'+esc((e&&e.message)||String(e))+'</div>';}).getPrivateFamilyLedgerForWeb();
}
function PRIVATE_monthLabel(k){const p=String(k).split("-");return new Date(+p[0],+p[1]-1,1).toLocaleDateString("en-US",{month:"long",year:"numeric"});}
function PRIVATE_effectiveSalary(k){
  const hist=(PRIVATE_data.salaryHistory||[]).slice().sort((a,b)=>String(a.effectiveMonth).localeCompare(String(b.effectiveMonth)));
  let v=0; hist.forEach(x=>{if(String(x.effectiveMonth)<=k)v=Number(x.amount||0);}); return v;
}
function PRIVATE_monthRows(k){return (PRIVATE_data.transactions||[]).filter(x=>String(x.monthKey)===k);}
function PRIVATE_given(k){return PRIVATE_monthRows(k).filter(x=>String(x.subCategory||"").trim().toLowerCase()==="priyanka salary").reduce((s,x)=>s+Number(x.amount||0),0);}
function PRIVATE_angel(k){return PRIVATE_monthRows(k).filter(x=>String(x.subCategory||"").trim().toLowerCase()==="angel one").reduce((s,x)=>s+Number(x.amount||0),0);}
function PRIVATE_tallied(k){return (PRIVATE_data.tallies||[]).filter(x=>String(x.monthKey)===k).reduce((s,x)=>s+Number(x.amount||0),0);}
function PRIVATE_kept(k){return Math.max(0,PRIVATE_effectiveSalary(k)-PRIVATE_given(k));}
function PRIVATE_allMonths(){
  const set=new Set((PRIVATE_data.transactions||[]).map(x=>x.monthKey).filter(Boolean));
  (PRIVATE_data.salaryHistory||[]).forEach(x=>set.add(x.effectiveMonth)); (PRIVATE_data.tallies||[]).forEach(x=>set.add(x.monthKey));
  if(PRIVATE_monthKey)set.add(PRIVATE_monthKey); return Array.from(set).sort();
}
function PRIVATE_holdingBefore(k){return PRIVATE_allMonths().filter(m=>m<k).reduce((s,m)=>s+PRIVATE_kept(m),0);}
function PRIVATE_angelBefore(k){return PRIVATE_allMonths().filter(m=>m<k).reduce((s,m)=>s+PRIVATE_angel(m)-PRIVATE_tallied(m),0);}
function PRIVATE_setTab(t){PRIVATE_tab=t;PRIVATE_render();}
function PRIVATE_saveSalary(){
  const m=document.getElementById("privateSalaryMonth").value,a=Number(document.getElementById("privateSalaryAmount").value||0); if(!m||a<0)return;
  google.script.run.withSuccessHandler(function(){PRIVATE_monthKey=m;PRIVATE_load();}).savePrivatePriyankaSalaryForWeb(m,a);
}
function PRIVATE_addTally(){
  const m=document.getElementById("privateTallyMonth").value,a=Number(document.getElementById("privateTallyAmount").value||0),n=document.getElementById("privateTallyNote").value||""; if(!m||a<=0)return;
  google.script.run.withSuccessHandler(function(){PRIVATE_monthKey=m;PRIVATE_load();}).addPrivateAngelTallyForWeb(m,a,n);
}
function PRIVATE_render(){
  const host=document.getElementById("roomArea");if(!host||!PRIVATE_data)return;
  let h='<button class="secondary" onclick="ROOM_backHome()">← Room</button><div class="view-section-title"><h2>🔐 Family Private Ledger</h2><p class="muted">One-way only: Money → this ledger. Nothing saved here changes Money, balances, Sharing or Gifts.</p></div>'+
    '<div class="private-tabs"><button class="private-tab '+(PRIVATE_tab==="monthly"?'active':'')+'" onclick="PRIVATE_setTab(\'monthly\')">Monthly</button><button class="private-tab '+(PRIVATE_tab==="yearly"?'active':'')+'" onclick="PRIVATE_setTab(\'yearly\')">Yearly</button></div>';
  if(PRIVATE_tab==="yearly") h+=PRIVATE_renderYearly(); else h+=PRIVATE_renderMonthly(); host.innerHTML=h;
}
function PRIVATE_renderMonthly(){
  const months=PRIVATE_allMonths().slice().reverse(); if(!months.includes(PRIVATE_monthKey)&&months.length)PRIVATE_monthKey=months[0]; const k=PRIVATE_monthKey;
  const actual=PRIVATE_effectiveSalary(k),given=PRIVATE_given(k),kept=PRIVATE_kept(k),prev=PRIVATE_holdingBefore(k),overall=prev+kept;
  const angel=PRIVATE_angel(k),tallied=PRIVATE_tallied(k),prevDue=PRIVATE_angelBefore(k),due=Math.max(0,prevDue+angel-tallied);
  const rows=PRIVATE_monthRows(k), latest=Number(PRIVATE_data.latestOverallRemaining||0);
  let opts=months.map(m=>'<option value="'+m+'" '+(m===k?'selected':'')+'>'+esc(PRIVATE_monthLabel(m))+'</option>').join('');
  let h='<div class="private-form"><label>Month<select onchange="PRIVATE_monthKey=this.value;PRIVATE_render()">'+opts+'</select></label></div>'+
  '<div class="private-panel"><h3>👩 Priyanka Holding — '+esc(PRIVATE_monthLabel(k))+'</h3><div class="private-grid">'+
  '<div class="private-card"><span>Actual Salary</span><b>'+moneyFmt(actual)+'</b></div><div class="private-card"><span>Given to Rahavan</span><b>'+moneyFmt(given)+'</b></div><div class="private-card"><span>She Kept This Month</span><b class="private-good">'+moneyFmt(kept)+'</b></div><div class="private-card"><span>Previous Holding</span><b>'+moneyFmt(prev)+'</b></div><div class="private-card"><span>Overall Holding</span><b class="private-secret">'+moneyFmt(overall)+'</b></div></div>'+
  '<div class="private-form"><label>Salary effective from<input id="privateSalaryMonth" type="month" value="'+k+'"></label><label>Priyanka actual salary<input id="privateSalaryAmount" type="number" min="0" step="0.01" value="'+actual+'"></label><button class="primary" onclick="PRIVATE_saveSalary()">Save Salary</button><span class="muted">This salary continues for later months until you change it again.</span></div></div>'+
  '<div class="private-panel"><h3>🔒 My Private / Angel One Tally</h3><div class="private-grid"><div class="private-card"><span>Current Overall Remaining</span><b>'+moneyFmt(latest)+'</b></div><div class="private-card"><span>Angel One Taken This Month</span><b>'+moneyFmt(angel)+'</b></div><div class="private-card"><span>Tallied / Put Back This Month</span><b>'+moneyFmt(tallied)+'</b></div><div class="private-card"><span>Still To Restore / Tally</span><b class="private-warn">'+moneyFmt(due)+'</b></div></div>'+
  '<div class="room-split-note"><b>Meaning:</b> Angel One is treated as private money moved out of tracked cash. Example: Remaining ₹10,000 and Angel One ₹100 → tracked cash becomes ₹9,900 and ₹100 stays in <b>Still To Restore / Tally</b>. Extra cash/profit/parents/overtime that was never entered in Money can be used later to tally it here without changing the main Money data.</div>'+
  '<div class="private-form"><label>Month<input id="privateTallyMonth" type="month" value="'+k+'"></label><label>Amount put back / tallied<input id="privateTallyAmount" type="number" min="0" step="0.01"></label><label>Private note<input id="privateTallyNote" type="text" placeholder="Profit / cash / overtime..."></label><button class="primary" onclick="PRIVATE_addTally()">Add Tally</button></div></div>'+
  '<div class="private-panel"><h3>Transactions — '+esc(PRIVATE_monthLabel(k))+'</h3>'+PRIVATE_txTable(rows)+'</div>';
  return h;
}
function PRIVATE_renderYearly(){
  const years=Array.from(new Set(PRIVATE_allMonths().map(m=>m.slice(0,4)))).sort().reverse(); if(!years.includes(PRIVATE_year)&&years.length)PRIVATE_year=years[0];
  let opts=years.map(y=>'<option '+(y===PRIVATE_year?'selected':'')+'>'+y+'</option>').join(''); let running=PRIVATE_allMonths().filter(m=>m.slice(0,4)<PRIVATE_year).reduce((s,m)=>s+PRIVATE_kept(m),0); let due=PRIVATE_allMonths().filter(m=>m.slice(0,4)<PRIVATE_year).reduce((s,m)=>s+PRIVATE_angel(m)-PRIVATE_tallied(m),0);
  let rows=''; for(let mo=1;mo<=12;mo++){const k=PRIVATE_year+'-'+String(mo).padStart(2,'0'),a=PRIVATE_effectiveSalary(k),g=PRIVATE_given(k),keep=PRIVATE_kept(k),ang=PRIVATE_angel(k),tal=PRIVATE_tallied(k);running+=keep;due+=ang-tal;rows+='<tr onclick="PRIVATE_monthKey=\''+k+'\';PRIVATE_tab=\'monthly\';PRIVATE_render()" style="cursor:pointer"><td>'+esc(PRIVATE_monthLabel(k))+'</td><td>'+moneyFmt(a)+'</td><td>'+moneyFmt(g)+'</td><td>'+moneyFmt(keep)+'</td><td><b>'+moneyFmt(running)+'</b></td><td>'+moneyFmt(ang)+'</td><td>'+moneyFmt(tal)+'</td><td><b>'+moneyFmt(Math.max(0,due))+'</b></td></tr>';}
  return '<div class="private-form"><label>Year<select onchange="PRIVATE_year=this.value;PRIVATE_render()">'+opts+'</select></label></div><div class="private-panel"><h3>Yearly Family Private Summary — '+esc(PRIVATE_year)+'</h3><div class="private-table"><table><thead><tr><th>Month</th><th>Priyanka Actual Salary</th><th>Given to Rahavan</th><th>She Kept</th><th>Overall Holding</th><th>Angel One Taken</th><th>Tallied</th><th>Still To Restore</th></tr></thead><tbody>'+rows+'</tbody></table></div><p class="muted">Click any month to open its monthly transactions.</p></div>';
}
function PRIVATE_txTable(rows){
  if(!rows.length)return '<p class="muted">No Money transactions for this month.</p>';
  return '<div class="private-table"><table><thead><tr><th>Date</th><th>Main</th><th>Sub Category</th><th>Explanation</th><th>Amount</th><th>Account</th></tr></thead><tbody>'+rows.map(x=>'<tr><td>'+esc(x.date||'')+'</td><td>'+esc(x.mainCategory||'')+'</td><td><b>'+esc(x.subCategory||'')+'</b></td><td>'+esc(x.explanation||'')+'</td><td>'+moneyFmt(x.amount)+'</td><td>'+esc(x.account||'')+'</td></tr>').join('')+'</tbody></table></div>';
}

/* ---------------- OPTION 3: All category totals ---------------- */
/* ---------------- OPTION 3: Period Summary ---------------- */
let option3PeriodType="daily";

function openViewMode3(){
  document.getElementById("viewModeChooser").style.display="none";
  document.getElementById("viewModeContent").innerHTML=
    '<button class="secondary" onclick="backToViewOptions()">← Back</button>'+
    '<div class="view-section-title">'+
      '<h2>📊 Period Summary</h2>'+
      '<p class="muted">View your money summary by Daily, Monthly or Yearly period.</p>'+
    '</div>'+
    '<div class="period-tabs">'+
      '<button class="period-tab active" onclick="showOption3Period(\'daily\',this)">Daily</button>'+
      '<button class="period-tab" onclick="showOption3Period(\'monthly\',this)">Monthly</button>'+
      '<button class="period-tab" onclick="showOption3Period(\'yearly\',this)">Yearly</button>'+
    '</div>'+
    '<div id="option3PeriodArea"></div>';

  showOption3Period("daily",document.querySelector("#viewModeContent .period-tab"));
}

function option3Bucket(){
  return {
    income:0,
    expenses:0,
    saving:0,
    others:0
  };
}

function addToOption3Bucket(bucket,x){
  const a=amountNumber(x.amount);
  const flow=cashFlowBucketForEntry(x);

  if(flow==="Income"){
    bucket.income+=a;
  }else if(flow==="Needs" || flow==="Wants"){
    bucket.expenses+=a;
  }else if(flow==="Savings"){
    bucket.saving+=a;
  }else{
    // Keep transfer / loan / miscellaneous movement in Others for this old-style summary.
    // Use signed cash effect so In / Loan In are positive and Out / Loan Out are negative.
    bucket.others+=cashEffectForEntry(x);
  }
}

function showOption3Period(type,btn){
  option3PeriodType=type;

  document.querySelectorAll("#viewModeContent .period-tab").forEach(function(x){
    x.classList.remove("active");
  });
  if(btn)btn.classList.add("active");

  const groups={};

  moneyEntries().forEach(function(x){
    const d=moneyReportingDate(x);
    if(!d)return;

    let key="",label="",day="";

    if(type==="daily"){
      key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
      label=String(d.getDate()).padStart(2,"0")+"-"+d.toLocaleDateString("en-US",{month:"short"})+"-"+d.getFullYear();
      day=d.toLocaleDateString("en-US",{weekday:"short"});
    }else if(type==="monthly"){
      key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0");
      label=d.toLocaleDateString("en-US",{month:"short"})+"-"+d.getFullYear();
    }else{
      key=String(d.getFullYear());
      label=key;
    }

    if(!groups[key]){
      groups[key]={
        key:key,
        label:label,
        day:day,
        data:option3Bucket()
      };
    }

    addToOption3Bucket(groups[key].data,x);
  });

  const rows=Object.keys(groups).sort().reverse().map(function(k){
    const r=groups[k];
    let endDate=null;
    if(type==="daily"){
      const p=k.split("-");
      endDate=new Date(Number(p[0]),Number(p[1])-1,Number(p[2]));
    }else if(type==="monthly"){
      const p=k.split("-");
      endDate=new Date(Number(p[0]),Number(p[1]),0);
    }else{
      endDate=new Date(Number(k),11,31);
    }
    r.cumulativeRemaining=moneyCumulativeBalanceAt(endDate);
    const periodRows=moneyEntries().filter(function(x){
      const d=moneyReportingDate(x); if(!d)return false;
      if(type==="daily")return RV_key(d)===k;
      if(type==="monthly")return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")===k;
      return String(d.getFullYear())===k;
    });
    r.flowTotals=moneyFlowTotals(periodRows);
    return r;
  });

  renderOption3PeriodTable(type,rows);
}

function renderOption3PeriodTable(type,rows){
  const area=document.getElementById("option3PeriodArea");
  if(!area)return;

  if(!rows.length){
    area.innerHTML='<div class="card"><p class="muted">No money data available.</p></div>';
    return;
  }

  const firstHeading=type==="daily"?"Date":type==="monthly"?"Monthly":"Yearly";
  const dayHeading=type==="daily"?'<th>Day</th>':'';

  // Overall totals for the currently selected Daily / Monthly / Yearly view.
  const totals=rows.reduce(function(t,r){
    t.income+=r.data.income;
    t.expenses+=r.data.expenses;
    t.saving+=r.data.saving;
    t.others+=r.data.others;
    return t;
  },{income:0,expenses:0,saving:0,others:0});

  const selectedRows=[];
  rows.forEach(function(r){
    if(r.flowTotals){
      selectedRows.push({totalIn:r.flowTotals.totalIn,totalOut:r.flowTotals.totalOut});
    }
  });
  const totalIn=selectedRows.reduce(function(s,r){return s+r.totalIn;},0);
  const totalOut=selectedRows.reduce(function(s,r){return s+r.totalOut;},0);
  totals.remaining=rows.length ? Number(rows[0].cumulativeRemaining||0) : moneyLatestCumulativeBalance();

  const totalCards=
    '<div class="option3-total-grid">'+
      '<div class="option3-total income-total"><span>Total In</span><b>'+moneyFmt(totalIn)+'</b></div>'+
      '<div class="option3-total expense-total"><span>Total Out</span><b>'+moneyFmt(totalOut)+'</b></div>'+
      '<div class="option3-total saving-total"><span>Savings</span><b>'+moneyFmt(totals.saving)+'</b></div>'+
      '<div class="option3-total others-total"><span>Other Movement</span><b>'+moneyFmt(totals.others)+'</b></div>'+
      '<div class="option3-total balance-total"><span>Overall Remaining</span><b>'+moneyFmt(totals.remaining)+'</b></div>'+
    '</div>';

  const body=rows.map(function(r){
    const d=r.data;

    // In/Out are for this period only. Remaining is cumulative through period end.
    const remaining=Number(r.cumulativeRemaining||0);

    return '<tr>'+
      '<td>'+esc(r.label)+'</td>'+
      (type==="daily"?'<td>'+esc(r.day)+'</td>':'')+
      '<td class="money-positive">'+moneyFmt(d.income)+'</td>'+
      '<td class="money-negative">'+moneyFmt(d.expenses)+'</td>'+
      '<td class="money-saving">'+moneyFmt(d.saving)+'</td>'+
      '<td class="'+(d.others>=0?'money-positive':'money-negative')+'">'+moneyFmt(d.others)+'</td>'+
      '<td class="'+(remaining>=0?'money-positive':'money-negative')+'">'+moneyFmt(remaining)+'</td>'+
    '</tr>';
  }).join('');

  area.innerHTML=
    '<div class="card option3-summary-card">'+
      '<h3>'+(
        type==="daily" ? "Daily Summary" :
        type==="monthly" ? "Monthly Summary" :
        "Yearly Summary"
      )+'</h3>'+
      totalCards+
      '<div class="option3-period-table-wrap">'+
        '<table class="option3-period-table">'+
          '<thead><tr>'+
            '<th>'+firstHeading+'</th>'+
            dayHeading+
            '<th>Income</th>'+
            '<th>Expenses</th>'+
            '<th>Saving</th>'+
            '<th>Others</th>'+
            '<th>Remaining Amount</th>'+
          '</tr></thead>'+
          '<tbody>'+body+'</tbody>'+
        '</table>'+
      '</div>'+
    '</div>';
}


let activeMoneyCategoryView = "";
let activeMoneySubcategoryView = "Overall";

function openMoneyCategoryTransactions(type){
  activeMoneyCategoryView = type;
  activeMoneySubcategoryView = "Overall";
  const win=document.getElementById("moneyCategoryTransactionsWindow");
  if(win)win.style.display="flex";

  const search=document.getElementById("moneyCategorySearch");
  if(search)search.value="";

  renderMoneyCategoryTransactions();
}

function closeMoneyCategoryTransactions(){
  const win=document.getElementById("moneyCategoryTransactionsWindow");
  if(win)win.style.display="none";
}


function dashboardCategoryForEntry(x){
  const g=String(x.mainCategory||"").trim().toLowerCase();
  const sub=String(x.subCategory||"").trim().toLowerCase();

  // Transfers are cash movements, not Income/Expenses.
  if(sub==="transfer in" || g==="in") return "Transfer";
  if(sub==="transfer out" || g==="transfer out" || g==="out") return "Transfer";

  // Loans are cash movements, not normal Income/Expenses.
  if(g==="loan in" || g==="loan i took" || g==="loan out" || g==="loan i out" || g==="loan i gave"){
    return "Loan";
  }

  if(g==="income") return "Income";
  if(g==="needs" || g==="wants") return "Expenses";
  if(g==="savings" || g==="saving") return "Savings";
  return "Others";
}

function cashFlowBucketForEntry(x){
  const g=String(x.mainCategory||"").trim().toLowerCase();
  const sub=String(x.subCategory||"").trim().toLowerCase();

  // Transfer directions
  if(sub==="transfer in" || g==="in") return "In";
  if(sub==="transfer out" || g==="transfer out" || g==="out") return "Out";

  // New help-sheet loan structure
  if(g==="loan in") return "Loan In";
  if(g==="loan out" || g==="loan i out") return "Loan Out";

  // Historical loan structure
  if(g==="loan i took"){
    if(sub.includes("repayment") && (sub.includes("paid") || sub.includes("given"))) return "Loan Out";
    return "Loan In";
  }
  if(g==="loan i gave"){
    if(sub.includes("repayment") || sub.includes("received")) return "Loan In";
    return "Loan Out";
  }

  if(g==="income") return "Income";
  if(g==="needs") return "Needs";
  if(g==="wants") return "Wants";
  if(g==="savings" || g==="saving") return "Savings";
  if(g==="savings return") return "Savings Return";
  return "Others";
}

function cashEffectForEntry(x){
  if(String(x.mainCategory||"").trim().toLowerCase()==="buffer") return 0;
  const a=amountNumber(x.amount);
  const flow=cashFlowBucketForEntry(x);

  // ONE RULE USED EVERYWHERE:
  // IN  = Income + In + Loan In + Savings Return
  // OUT = Needs + Wants + Savings + Out + Others + Loan Out
  if(flow==="Income" || flow==="In" || flow==="Loan In" || flow==="Savings Return") return a;
  if(flow==="Needs" || flow==="Wants" || flow==="Savings" || flow==="Out" || flow==="Others" || flow==="Loan Out") return -a;
  return 0;
}

function moneyIsInEntry(x){
  const f=cashFlowBucketForEntry(x);
  return f==="Income" || f==="In" || f==="Loan In" || f==="Savings Return";
}
function moneyIsOutEntry(x){
  const f=cashFlowBucketForEntry(x);
  return f==="Needs" || f==="Wants" || f==="Savings" || f==="Out" || f==="Others" || f==="Loan Out";
}
function moneyFlowTotals(rows){
  let totalIn=0,totalOut=0;
  (rows||[]).forEach(function(x){
    const a=amountNumber(x.amount);
    if(moneyIsInEntry(x)) totalIn+=a;
    else if(moneyIsOutEntry(x)) totalOut+=a;
  });
  return {totalIn:totalIn,totalOut:totalOut,net:totalIn-totalOut};
}
function moneySortChronological(rows){
  return (rows||[]).slice().sort(function(a,b){
    const da=parseTrackerDate(a.date), db=parseTrackerDate(b.date);
    const ta=da?da.getTime():0, tb=db?db.getTime():0;
    if(ta!==tb)return ta-tb;
    const oa=Number(a.order||0), ob=Number(b.order||0);
    if(oa!==ob)return oa-ob;
    return Number(a.sheetRow||0)-Number(b.sheetRow||0);
  });
}
function moneySheetOverallRemainingAt(dateLike){
  const target=dateLike instanceof Date ? dateLike : parseTrackerDate(dateLike);
  if(!target)return 0;
  const end=new Date(target.getFullYear(),target.getMonth(),target.getDate(),23,59,59,999);
  const rows=moneySortChronological(moneyEntries()).filter(function(x){
    const d=parseTrackerDate(x.date);
    return d && d<=end;
  });
  for(let i=rows.length-1;i>=0;i--){
    const raw=(rows[i].overallRemainingRaw!==undefined)?rows[i].overallRemainingRaw:rows[i].overallRemaining;
    const n=typeof sheetMoneyNumber==="function"
      ? sheetMoneyNumber(raw)
      : Number(String(raw==null?"":raw).replace(/[₹,\\s]/g,""));
    if(n!==null && Number.isFinite(Number(n)))return Number(n);
  }
  return 0;
}
function moneyCumulativeBalanceAt(dateLike){
  return moneySheetOverallRemainingAt(dateLike);
}
function moneyLatestCumulativeBalance(){
  const rows=moneySortChronological(moneyEntries());
  for(let i=rows.length-1;i>=0;i--){
    const raw=(rows[i].overallRemainingRaw!==undefined)?rows[i].overallRemainingRaw:rows[i].overallRemaining;
    const n=typeof sheetMoneyNumber==="function"
      ? sheetMoneyNumber(raw)
      : Number(String(raw==null?"":raw).replace(/[₹,\\s]/g,""));
    if(n!==null && Number.isFinite(Number(n)))return Number(n);
  }
  return 0;
}
function moneyMaxDate(rows){
  let out=null;
  (rows||[]).forEach(function(x){
    const d=moneyReportingDate(x);
    if(d && (!out || d>out))out=d;
  });
  return out;
}

function loanRelationshipForEntry(x){
  const sub=String(x.subCategory||"").trim().toLowerCase().replace(/\s+/g," ");
  if(sub==="loan received") return "Loan I Took";
  if(sub==="loan repayment paid") return "Loan I Took";
  if(sub==="loan i gave" || sub==="money lent") return "Loan I Gave";
  if(sub==="loan repayment received") return "Loan I Gave";
  return "";
}
function loanOutstandingEffect(x,type){
  const sub=String(x.subCategory||"").trim().toLowerCase().replace(/\s+/g," ");
  const a=amountNumber(x.amount);
  if(type==="Loan I Took"){
    if(sub==="loan received") return a;
    if(sub==="loan repayment paid") return -a;
  }
  if(type==="Loan I Gave"){
    if(sub==="loan i gave" || sub==="money lent") return a;
    if(sub==="loan repayment received") return -a;
  }
  return 0;
}
function moneyCategoryMatches(x,type){
  const g=dashboardCategoryForEntry(x);
  const flow=cashFlowBucketForEntry(x);
  if(type==="Expenses") return g==="Expenses";
  if(type==="Savings") return flow==="Savings" || flow==="Savings Return";
  if(type==="Loan I Took" || type==="Loan I Gave") return loanRelationshipForEntry(x)===type;
  return g===type;
}
function moneyCategoryColorClass(type){
  if(type==="Income")return "cat-income";
  if(type==="Expenses")return "cat-expense";
  if(type==="Savings")return "cat-saving";
  if(type==="Loan I Took")return "cat-loan-took";
  if(type==="Loan I Gave")return "cat-loan-gave";
  return "";
}



function savingsBaseSubCategory(x){
  const flow=cashFlowBucketForEntry(x);
  const raw=String(x.subCategory||"Uncategorized").trim() || "Uncategorized";
  if(flow!=="Savings Return") return raw;

  const k=raw.toLowerCase().replace(/\s+/g," ").trim();
  if(k==="f/d maturity" || k==="fd maturity" || k==="f/d after maturity") return "F/d";
  if(k==="ppf withdrawal") return "PPF";
  if(k==="gold sale") return "Gold";
  if(k==="stock withdrawal" || k==="stocks withdrawal" || k==="stock sale") return "stocks";
  return raw;
}

function savingsSignedAmount(x){
  const a=amountNumber(x.amount);
  return cashFlowBucketForEntry(x)==="Savings Return" ? -a : a;
}

function renderMoneySubcategoryTabs(baseData){
  const tabs=document.getElementById("moneySubcategoryTabs");
  if(!tabs)return;

  const isSavingsView=(activeMoneyCategoryView==="Savings");
  const totals={};

  baseData.forEach(function(x){
    const sub=isSavingsView ? savingsBaseSubCategory(x) : (String(x.subCategory||"Uncategorized").trim() || "Uncategorized");
    const amt=isSavingsView ? savingsSignedAmount(x) : amountNumber(x.amount);
    totals[sub]=(totals[sub]||0)+amt;
  });

  const subs=Object.keys(totals).sort(function(a,b){
    return totals[b]-totals[a];
  });

  const isLoanView=(activeMoneyCategoryView==="Loan I Took" || activeMoneyCategoryView==="Loan I Gave");
  const overallTotal=baseData.reduce(function(sum,x){
    if(isSavingsView) return sum+savingsSignedAmount(x);
    if(isLoanView) return sum+loanOutstandingEffect(x,activeMoneyCategoryView);
    return sum+amountNumber(x.amount);
  },0);

  let html=
    '<button class="subcategory-tab '+(activeMoneySubcategoryView==="Overall"?"active":"")+'" onclick="selectMoneySubcategory(\'Overall\')">'+
      '<b>Overall</b><span>'+moneyFmt(overallTotal)+'</span>'+
    '</button>';

  html+=subs.map(function(sub){
    return '<button class="subcategory-tab '+(activeMoneySubcategoryView===sub?"active":"")+'" onclick="selectMoneySubcategory(\''+esc(sub).replace(/'/g,"\\'")+'\')">'+
      '<b>'+esc(sub)+'</b><span>'+moneyFmt(totals[sub])+'</span>'+
    '</button>';
  }).join("");

  tabs.innerHTML=html;
}

function selectMoneySubcategory(sub){
  activeMoneySubcategoryView=sub;
  renderMoneyCategoryTransactions();
}

function renderMoneyCategoryTransactions(){
  const type=activeMoneyCategoryView;
  const title=document.getElementById("moneyCategoryTransactionsTitle");
  const summary=document.getElementById("moneyCategoryTransactionsSummary");
  const box=document.getElementById("moneyCategoryTransactionsTable");
  if(!box)return;

  const q=String(document.getElementById("moneyCategorySearch")?.value||"").trim().toLowerCase();

  const baseData=moneyEntries().filter(function(x){
    return moneyCategoryMatches(x,type);
  });

  renderMoneySubcategoryTabs(baseData);

  let data=baseData;

  if(activeMoneySubcategoryView!=="Overall"){
    data=data.filter(function(x){
      return String(x.subCategory||"Uncategorized").trim()===activeMoneySubcategoryView;
    });
  }

  if(q){
    data=data.filter(function(x){
      return [
        x.date,x.day,x.mainCategory,x.subCategory,x.explanation,x.account,x.fromAccount
      ].some(function(v){
        return String(v||"").toLowerCase().includes(q);
      });
    });
  }

  data.sort(function(a,b){
    const da=parseTrackerDate(a.date), db=parseTrackerDate(b.date);
    return (db?db.getTime():0)-(da?da.getTime():0);
  });

  const isLoanView=(type==="Loan I Took" || type==="Loan I Gave");
  const total=data.reduce(function(sum,x){
    if(isLoanView && activeMoneySubcategoryView==="Overall") return sum+loanOutstandingEffect(x,type);
    return sum+amountNumber(x.amount);
  },0);

  if(title){
    title.textContent =
      (type==="Income"?"💵 ":
       type==="Expenses"?"💸 ":
       type==="Savings"?"🏦 ":
       type==="Loan I Took"?"📥 ":"📤 ") + type + " Transactions";
  }

  if(summary){
    summary.innerHTML=
      '<b>'+esc(activeMoneySubcategoryView)+'</b> &nbsp; • &nbsp; '+
      '<b>'+data.length+' transactions</b> &nbsp; • &nbsp; '+
      'Total: <b>'+moneyFmt(total)+'</b>';
  }

  if(!data.length){
    box.innerHTML='<div class="card"><p class="muted">No '+esc(activeMoneySubcategoryView)+' transactions found.</p></div>';
    return;
  }

  box.innerHTML=
    '<div class="category-table-wrap">'+
      '<table class="category-transaction-table '+moneyCategoryColorClass(type)+'">'+
        '<thead><tr>'+
          '<th>Date</th>'+
          '<th>Day</th>'+
          '<th>Sub Category</th>'+
          '<th>Explanation</th>'+
          '<th>Amount</th>'+
          '<th>Account</th>'+
        '</tr></thead>'+
        '<tbody>'+
          data.map(function(x){
            return '<tr>'+
              '<td>'+esc(x.date||"")+'</td>'+
              '<td>'+esc(x.day||"")+'</td>'+
              '<td><b>'+esc(x.subCategory||"")+'</b></td>'+
              '<td>'+esc(x.explanation||"")+'</td>'+
              '<td class="transaction-amount">'+moneyFmt(x.amount)+'</td>'+
              '<td>'+esc(x.account||x.fromAccount||"")+'</td>'+
            '</tr>';
          }).join('')+
        '</tbody>'+
      '</table>'+
    '</div>';
}



function openMoneyForecast(){
  const win=document.getElementById("moneyForecastWindow");
  if(win)win.style.display="flex";

  const now=new Date();
  const next=new Date(now.getFullYear(),now.getMonth()+1,1);
  const monthValue=next.getFullYear()+"-"+String(next.getMonth()+1).padStart(2,"0");
  const monthInput=document.getElementById("forecastMonth");
  if(monthInput && !monthInput.value)monthInput.value=monthValue;

  renderMoneyForecast();
}

function closeMoneyForecast(){
  const win=document.getElementById("moneyForecastWindow");
  if(win)win.style.display="none";
}

function monthBucketKey(d){
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0");
}

function monthBucketLabel(key){
  const parts=key.split("-");
  const d=new Date(Number(parts[0]),Number(parts[1])-1,1);
  return d.toLocaleDateString("en-US",{month:"short",year:"numeric"});
}

function buildForecastMonthlyHistory(){
  const map={};

  moneyEntries().forEach(function(x){
    const d=moneyReportingDate(x);
    if(!d)return;

    const key=monthBucketKey(d);
    if(!map[key]){
      map[key]={
        income:0,needs:0,wants:0,saving:0,
        loanIn:0,loanOut:0
      };
    }

    const flow=cashFlowBucketForEntry(x);
    const a=amountNumber(x.amount);

    if(flow==="Income")map[key].income+=a;
    else if(flow==="Needs")map[key].needs+=a;
    else if(flow==="Wants")map[key].wants+=a;
    else if(flow==="Savings")map[key].saving+=a;
    else if(flow==="Loan In")map[key].loanIn+=a;
    else if(flow==="Loan Out")map[key].loanOut+=a;
  });

  return Object.keys(map).sort().map(function(key){
    return {key:key,label:monthBucketLabel(key),...map[key]};
  });
}

function averageForecastFields(rows){
  if(!rows.length){
    return {income:0,needs:0,wants:0,saving:0,loanIn:0,loanOut:0};
  }

  const sum={income:0,needs:0,wants:0,saving:0,loanIn:0,loanOut:0};
  rows.forEach(function(r){
    Object.keys(sum).forEach(function(k){
      sum[k]+=Number(r[k]||0);
    });
  });

  Object.keys(sum).forEach(function(k){
    sum[k]=sum[k]/rows.length;
  });

  return sum;
}

function renderMoneyForecast(){
  const history=buildForecastMonthlyHistory();
  const lookback=Number(document.getElementById("forecastLookback")?.value||3);
  const recent=history.slice(-lookback);
  const avg=averageForecastFields(recent);

  const fields={
    fcIncome:avg.income,
    fcNeeds:avg.needs,
    fcWants:avg.wants,
    fcSavings:avg.saving,
    fcLoanIn:avg.loanIn,
    fcLoanOut:avg.loanOut
  };

  Object.keys(fields).forEach(function(id){
    const el=document.getElementById(id);
    if(el)el.value=Math.round(fields[id]*100)/100;
  });

  renderForecastHistory(recent);
  recalculateForecastFromInputs();
}

function recalculateForecastFromInputs(){
  const current=Number(moneyTotals().Remaining||0);
  const reserve=Number(document.getElementById("forecastReserve")?.value||0);

  const income=Number(document.getElementById("fcIncome")?.value||0);
  const needs=Number(document.getElementById("fcNeeds")?.value||0);
  const wants=Number(document.getElementById("fcWants")?.value||0);
  const savings=Number(document.getElementById("fcSavings")?.value||0);
  const loanIn=Number(document.getElementById("fcLoanIn")?.value||0);
  const loanOut=Number(document.getElementById("fcLoanOut")?.value||0);

  // Free cash excludes discretionary Wants so it shows room before optional spending.
  const freeCash=income+loanIn-needs-savings-loanOut;
  const projected=current+income+loanIn-needs-wants-savings-loanOut;
  const safeToSpend=Math.max(0, projected-reserve);

  const put=function(id,val){
    const el=document.getElementById(id);
    if(el)el.textContent=moneyFmt(val);
  };

  put("forecastCurrentBalance",current);
  put("forecastFreeCash",freeCash);
  put("forecastSafeSpend",safeToSpend);
  put("forecastEndBalance",projected);

  put("fcFormulaStart",current);
  put("fcFormulaIncome",income);
  put("fcFormulaLoanIn",loanIn);
  put("fcFormulaNeeds",needs);
  put("fcFormulaWants",wants);
  put("fcFormulaSavings",savings);
  put("fcFormulaLoanOut",loanOut);
  put("fcFormulaEnd",projected);

  const endEl=document.getElementById("forecastEndBalance");
  const safeEl=document.getElementById("forecastSafeSpend");
  if(endEl)endEl.style.color=projected>=reserve?"#15803d":"#dc2626";
  if(safeEl)safeEl.style.color=safeToSpend>0?"#15803d":"#dc2626";

  const decision=document.getElementById("forecastDecision");
  if(decision){
    let cls="good",title="",text="";

    if(projected<0){
      cls="bad";
      title="Reconsider major purchases";
      text="Your projected balance goes below ₹0. Reduce Wants, Savings, or other planned outflows before adding a new purchase.";
    }else if(projected<reserve){
      cls="warn";
      title="Purchase with caution";
      text="Your projected balance stays positive but falls below your minimum reserve of "+moneyFmt(reserve)+".";
    }else if(safeToSpend>0){
      cls="good";
      title="Within your current plan";
      text="Based on your recent pattern, you can spend up to about "+moneyFmt(safeToSpend)+" and still finish the month at or above your reserve.";
    }else{
      cls="warn";
      title="No extra spending room";
      text="Your plan uses nearly all available cash above your reserve. Consider postponing optional purchases.";
    }

    decision.className="forecast-decision "+cls;
    decision.innerHTML="<b>"+title+"</b><span>"+text+"</span>";
  }
}

function renderForecastHistory(rows){
  const box=document.getElementById("forecastHistoryTable");
  if(!box)return;

  if(!rows.length){
    box.innerHTML='<p class="muted">No monthly history available yet.</p>';
    return;
  }

  box.innerHTML=
    '<div style="overflow:auto"><table class="forecast-history-table">'+
      '<thead><tr>'+
        '<th>Month</th><th>Income</th><th>Needs</th><th>Wants</th><th>Savings</th><th>Loan In</th><th>Loan Out</th>'+
      '</tr></thead><tbody>'+
      rows.slice().reverse().map(function(r){
        return '<tr>'+
          '<td>'+esc(r.label)+'</td>'+
          '<td class="money-positive">'+moneyFmt(r.income)+'</td>'+
          '<td class="money-negative">'+moneyFmt(r.needs)+'</td>'+
          '<td class="money-negative">'+moneyFmt(r.wants)+'</td>'+
          '<td class="money-saving">'+moneyFmt(r.saving)+'</td>'+
          '<td>'+moneyFmt(r.loanIn)+'</td>'+
          '<td>'+moneyFmt(r.loanOut)+'</td>'+
        '</tr>';
      }).join('')+
      '</tbody></table></div>';
}

function openUploadWindow(){
  document.getElementById("uploadWindow").style.display="flex";
  document.getElementById("uploadChoiceArea").style.display="grid";
  document.getElementById("uploadWindowContent").innerHTML="";
}
function closeUploadWindow(){
  document.getElementById("uploadWindow").style.display="none";
}
function backToUploadChoices(){
  document.getElementById("uploadChoiceArea").style.display="grid";
  document.getElementById("uploadWindowContent").innerHTML="";
}
function showUploadSheetInsideWindow(){
  document.getElementById("uploadChoiceArea").style.display="none";
  document.getElementById("uploadWindowContent").innerHTML=
    '<div class="card"><button class="secondary" onclick="backToUploadChoices()">← Back</button>'+
    '<h3>📊 Sheet Upload</h3>'+
    '<label>Select your Google Sheet / Excel / CSV file<input id="moneyFileModal" type="file" accept=".xlsx,.xls,.csv"></label>'+
    '<div class="note"><b>Expected columns:</b><br>Date · Category · Explanation · Amount · Amount Category · Account · Remaining Amount</div>'+
    '<div id="uploadProgressModal" class="muted" style="margin-top:12px"></div></div>';

  document.getElementById("moneyFileModal").addEventListener("change", function(e){
    const originalProgress = document.getElementById("uploadProgress");
    const modalProgress = document.getElementById("uploadProgressModal");
    // Reuse the existing import engine directly.
    const file=e.target.files[0]; if(!file)return;
    modalProgress.textContent="Reading "+file.name+" ...";
    const reader=new FileReader();
    reader.onload=function(evt){
      try{
        let rows=[];
        if(file.name.toLowerCase().endsWith(".csv")){
          rows=parseCSV(evt.target.result);
        }else{
          if(typeof XLSX==="undefined") throw new Error("Excel reader could not load. Please use CSV or open with internet access.");
          const wb=XLSX.read(evt.target.result,{type:"array",cellDates:true});
          const ws=wb.Sheets[wb.SheetNames[0]];
          rows=XLSX.utils.sheet_to_json(ws,{defval:""});
        }
        // Store imported rows and refresh totals first.
        importMoneyRows(rows,file.name);
        modalProgress.innerHTML = "✓ " + rows.length + " rows are ready.<br>" +
  "<button class='primary' style='margin-top:10px' id='confirmSheetUploadBtn'>OK</button>";
document.getElementById("confirmSheetUploadBtn").onclick = function(){
  confirmSheetUpload(file.name, rows.length);
};
      }catch(err){
        modalProgress.textContent="Import failed: "+err.message;
      }
    };
    if(file.name.toLowerCase().endsWith(".csv")) reader.readAsText(file);
    else reader.readAsArrayBuffer(file);
  });
}
function showManualInsideWindow(){
  document.getElementById("uploadChoiceArea").style.display="none";
  document.getElementById("uploadWindowContent").innerHTML=
    '<button class="secondary" onclick="backToUploadChoices()">← Back</button>'+manualForm();
  updateSubCategories();
}

function moneySection(type){
 const box=document.getElementById("moneyModule");
 box.style.display="block";
 if(type==="Upload"){
  box.innerHTML='<h2>📤 Add Money Data</h2><p class="muted">Choose one method.</p><div class="option-grid">'+
  '<button class="option" onclick="sheetUpload()"><div class="option-icon">📊</div><b>Sheet Upload</b><p class="muted">Upload your existing Google Sheet, Excel or CSV.</p></button>'+
  '<button class="option" onclick="manualEntry()"><div class="option-icon">✍️</div><b>Manual Data Entry</b><p class="muted">Enter one transaction at a time.</p></button></div><div id="moneyEntryArea"></div>';
 }else{
  box.innerHTML='<h2>'+esc(type)+'</h2><p class="muted">Choose how you want to add '+esc(type)+' data.</p><div class="option-grid">'+
  '<button class="option" onclick="sheetUpload()"><div class="option-icon">📊</div><b>Sheet Upload</b><p class="muted">Upload '+esc(type)+' data.</p></button>'+
  '<button class="option" onclick="manualEntry()"><div class="option-icon">✍️</div><b>Manual Data Entry</b><p class="muted">Enter '+esc(type)+' manually.</p></button></div><div id="moneyEntryArea"></div>';
 }
 box.scrollIntoView({behavior:"smooth"});
}

function sheetUpload(){
 document.getElementById("moneyEntryArea").innerHTML='<div class="card">'+
 '<h3>📊 Sheet Upload</h3>'+
 '<label>Select your Google Sheet / Excel / CSV file<input id="moneyFile" type="file" accept=".xlsx,.xls,.csv"></label>'+
 '<div class="note"><b>Your sheet columns can be:</b><br>Date · Day · Category · Explanation · Amount · Amount Category · Account · Remaining Amount<br><br>'+
 '<b>Amount Category:</b> 1 = Income, 2 = Needs/Expense, 3 = Savings, 4 = Others, 5 = In, 6 = Wants/Expense, 7 = Out/Transfer.</div>'+
 '<div id="uploadProgress" class="muted" style="margin-top:12px"></div></div>';
 document.getElementById("moneyFile").addEventListener("change",handleMoneyFile);
}
function handleMoneyFile(e){
 const file=e.target.files[0]; if(!file)return;
 const status=document.getElementById("uploadProgress");
 status.textContent="Reading "+file.name+" ...";
 const reader=new FileReader();
 reader.onload=function(evt){
   try{
     let rows=[];
     if(file.name.toLowerCase().endsWith(".csv")){
       rows=parseCSV(evt.target.result);
     }else{
       if(typeof XLSX==="undefined") throw new Error("Excel reader could not load. Please use CSV or open this page with internet access.");
       const wb=XLSX.read(evt.target.result,{type:"array",cellDates:true});
       const ws=wb.Sheets[wb.SheetNames[0]];
       rows=XLSX.utils.sheet_to_json(ws,{defval:""});
     }
     importMoneyRows(rows,file.name);
     status.textContent="✓ Imported "+rows.length+" rows successfully.";
   }catch(err){
     status.textContent="Import failed: "+err.message;
     console.error(err);
   }
 };
 if(file.name.toLowerCase().endsWith(".csv")) reader.readAsText(file);
 else reader.readAsArrayBuffer(file);
}
function parseCSV(text){
 const lines=text.replace(/\r/g,"").split("\n").filter(x=>x.trim()!=="");
 if(!lines.length)return[];
 const parseLine=function(line){
   let out=[],cur="",quote=false;
   for(let i=0;i<line.length;i++){
     let c=line[i];
     if(c==='"'){
       if(quote && line[i+1]==='"'){cur+='"';i++} else quote=!quote;
     }else if(c===","&&!quote){out.push(cur.trim());cur=""}else cur+=c;
   }
   out.push(cur.trim());return out;
 };
 const headers=parseLine(lines[0]).map(x=>x.trim());
 return lines.slice(1).map(line=>{
   const vals=parseLine(line),o={};
   headers.forEach((h,i)=>o[h]=vals[i]??"");
   return o;
 });
}
function normKey(s){return String(s||"").toLowerCase().replace(/[^a-z0-9]/g,"")}
function getField(row,names){
 const keys=Object.keys(row);
 const normalized=keys.map(k=>({raw:k,n:normKey(k)}));
 for(const name of names){
   const target=normKey(name);
   const exact=normalized.find(x=>x.n===target);
   if(exact)return row[exact.raw];
 }
 // tolerate extra spaces/words in headers
 for(const name of names){
   const target=normKey(name);
   const partial=normalized.find(x=>x.n.includes(target)||target.includes(x.n));
   if(partial)return row[partial.raw];
 }
 return "";
}
function amountNumber(v){
 if(typeof v==="number" && isFinite(v))return Math.abs(v);
 let s=String(v??"").replace(/₹|Rs\.?|INR|,/gi,"").trim();
 if(!s)return 0;
 // Handles values such as "(1,250.50)" or "1,250.50 Dr"
 let neg=/^\(.*\)$/.test(s);
 s=s.replace(/[^\d.\-]/g,"");
 let n=parseFloat(s);
 if(isNaN(n))return 0;
 return Math.abs(n);
}
function categoryGroupFromNumber(n){
 const x=parseInt(String(n).trim(),10);
 return ({1:"Income",2:"Needs",3:"Savings",4:"Others",5:"In",6:"Wants",7:"Out"})[x]||"";
}
function findGroupForSubCategory(category){
 const c=String(category||"").trim().toLowerCase();
 for(const [group,items] of Object.entries(config.categories)){
   if(items.some(x=>String(x).trim().toLowerCase()===c))return group;
 }
 return "";
}
function formatSheetDate(v){
 if(v===null || v===undefined || v==="") return "";

 // SheetJS Date object
 if(Object.prototype.toString.call(v)==="[object Date]" && !isNaN(v.getTime())){
   return String(v.getDate()).padStart(2,"0")+"-"+String(v.getMonth()+1).padStart(2,"0")+"-"+v.getFullYear();
 }

 // Excel serial number
 if(typeof v==="number" && isFinite(v)){
   const d=new Date(Date.UTC(1899,11,30)+Math.floor(v)*86400000);
   return String(d.getUTCDate()).padStart(2,"0")+"-"+String(d.getUTCMonth()+1).padStart(2,"0")+"-"+d.getUTCFullYear();
 }

 const s=String(v).trim();

 // Excel serial saved as text
 if(/^\d{5}(?:\.\d+)?$/.test(s)){
   const d=new Date(Date.UTC(1899,11,30)+Math.floor(parseFloat(s))*86400000);
   return String(d.getUTCDate()).padStart(2,"0")+"-"+String(d.getUTCMonth()+1).padStart(2,"0")+"-"+d.getUTCFullYear();
 }

 return s;
}

function importMoneyRows(rows,fileName){
 let imported=[];
 rows.forEach((r,index)=>{
   // Read the columns exactly as they exist in your sheet.
   const mainCategory=String(getField(r,[
     "Main Category","Main Catageory","main category","main catageory"
   ])||"").trim();

   const subCategory=String(getField(r,[
     "Sub Category","Sub Catageory","sub category","sub catageory",
     "Category","Catageory","category","catageory"
   ])||"").trim();

   const explanation=String(getField(r,[
     "Explanation","Description","Narration"
   ])||"").trim();

   const amount=amountNumber(getField(r,["Amount","amount"]));

   // Keep rows that contain either category information or an amount.
   if(!mainCategory && !subCategory && !amount) return;

   const amountCat=getField(r,[
     "Amount Category","Amount Catageory","AmountCategory","amount category"
   ]);

   let group=mainCategory;
   if(!group) group=categoryGroupFromNumber(amountCat);
   if(!group) group=findGroupForSubCategory(subCategory);
   if(!group) group="Others";

   imported.push({
     source:"sheet",
     file:fileName,
     row:index+2,
     date:formatSheetDate(getField(r,["Date","date"])),
     day:getField(r,["Day","day"]),
     mainCategory:group,
     subCategory:subCategory,
     explanation:explanation,
     amount:amount,
     amountCategory:amountCat,
     account:getField(r,[
       "Amount spend on which account",
       "Amount spend on which Account",
       "Account","account","Bank"
     ]),
     remainingAmount:getField(r,["Remaining Amount","RemainingAmount"])
   });
 });

 // Replace old uploaded-sheet rows, but keep manual entries.
 let old=JSON.parse(localStorage.getItem("moneyEntries")||"[]");
 old=old.filter(x=>x.source!=="sheet");
 localStorage.setItem("moneyEntries",JSON.stringify(old.concat(imported)));
 localStorage.setItem("moneyLastImport",JSON.stringify({
   file:fileName,count:imported.length,date:new Date().toISOString()
 }));
 updateMoneyDashboard();
}

function manualEntry(){
  renderMoneyQuickEntry();
  const card=document.getElementById("moneyQuickEntryCard");
  if(card){
    card.scrollIntoView({behavior:"smooth",block:"start"});
  }
  setTimeout(function(){
    const amount=document.getElementById("mAmount");
    if(amount)amount.focus();
  },250);
}
function manualForm(){
  let groups=Object.keys(config.categories||{});
  let groupOptions=groups.map(function(g){
    return '<option value="'+esc(g)+'">'+esc(g)+'</option>';
  }).join("");

  let accountOptions=(config.accounts||[]).map(function(a){
    return '<option value="'+esc(a)+'">'+esc(a)+'</option>';
  }).join("");

  return '<div class="card">'+
    '<div class="form-grid">'+
      '<label>Date<input id="mDate" type="date" value="'+new Date().toISOString().slice(0,10)+'"></label>'+
      '<label>Amount<input id="mAmount" type="number" step="0.01" placeholder="0.00"></label>'+
      '<label>Main Category<select id="mMainCategory" onchange="updateSubCategories()">'+groupOptions+'</select></label>'+
      '<label>Sub Category<select id="mSubCategory"></select></label>'+
    '</div>'+
    '<div class="money-quick-line">'+
      '<label>Explanation<input id="mExplanation" placeholder="What was this transaction for?"></label>'+
      '<label>From Account<select id="mFromAccount">'+accountOptions+'</select></label>'+
      '<label>To Account <span class="muted">(optional)</span><select id="mToAccount"><option value="">Not applicable</option>'+accountOptions+'</select></label>'+
      '<label>Sharing <span class="muted">(optional)</span><input id="mSharing" list="roomSharingPeopleList" placeholder="Kapil or Kapil,Naveen"></label>'+
      '<div class="actions"><button class="primary" onclick="saveMoneyEntry()">💾 Save Entry</button></div>'+
    '</div>'+
    '<div class="note">Google Sheet date will be stored/displayed as <b>08-Nov-2026</b>. Main/Sub Categories come from the <b>help</b> sheet.</div>'+
  '</div>';
}

function renderMoneyQuickEntry(){
  const host=document.getElementById("moneyQuickEntry");
  if(!host)return;

  host.innerHTML=manualForm();
  updateSubCategories();
}

function refreshMoneyCategories(showMessage){
  const status=document.getElementById("moneyQuickCategoryStatus");
  if(status){
    status.textContent="Refreshing help sheet…";
    status.style.color="#64748b";
  }

  return new Promise(function(resolve,reject){
    if(typeof google==="undefined" || !google.script || !google.script.run){
      const msg="Google Apps Script connection unavailable.";
      if(status){status.textContent=msg;status.style.color="#dc2626";}
      reject(new Error(msg));
      return;
    }

    google.script.run
      .withSuccessHandler(function(result){
        if(!result || !result.success){
          const msg=(result&&result.message)||"Could not refresh help sheet.";
          if(status){status.textContent=msg;status.style.color="#dc2626";}
          if(showMessage)alert("Category refresh failed.\n"+msg);
          reject(new Error(msg));
          return;
        }

        const categories=result.categories||{};
        config.categories=categories;
        localStorage.setItem("moneyConfig",JSON.stringify(config));

        renderMoneyQuickEntry();

        if(status){
          const subCount=Object.keys(categories).reduce(function(sum,k){
            return sum+(Array.isArray(categories[k])?categories[k].length:0);
          },0);
          status.textContent="✓ "+Object.keys(categories).length+" categories · "+subCount+" sub categories";
          status.style.color="#15803d";
        }

        // Also refresh the Money Set window if it is open.
        const win=document.getElementById("moneySetWindow");
        if(win && win.style.display==="flex" && typeof renderMoneySet==="function"){
          renderMoneySet();
        }

        if(showMessage)alert("✓ Categories refreshed from the help sheet.");
        resolve(categories);
      })
      .withFailureHandler(function(err){
        const msg=(err&&err.message)?err.message:String(err);
        if(status){status.textContent="Refresh failed: "+msg;status.style.color="#dc2626";}
        if(showMessage)alert("Category refresh failed.\n"+msg);
        reject(err);
      })
      .refreshMoneySetForWeb();
  });
}

function updateSubCategories(){
 let main=document.getElementById("mMainCategory"),sub=document.getElementById("mSubCategory");
 if(!main||!sub)return;
 let items=config.categories[main.value]||[];
 sub.innerHTML=items.length?items.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join(""):'<option value="">No sub categories</option>';
}
async function saveMoneyEntry(){
 const entry={
   date:document.getElementById("mDate").value,
   mainCategory:document.getElementById("mMainCategory").value,
   subCategory:document.getElementById("mSubCategory").value,
   explanation:document.getElementById("mExplanation").value,
   amount:Number(document.getElementById("mAmount").value||0),
   account:document.getElementById("mFromAccount").value,
   fromAccount:document.getElementById("mFromAccount").value,
   toAccount:document.getElementById("mToAccount").value,
   sharing:(document.getElementById("mSharing")||{}).value||""
 };

 if(!entry.date || !entry.mainCategory || !entry.subCategory || !entry.amount){
   alert("Please enter Date, Main Category, Sub Category and Amount.");
   return;
 }

 try{
   setGoogleSyncStatus("Saving transaction to Google Sheet...",null);

   // 1) Save to Google Sheet first.
   const result=await addTransactionToGoogleSheet(entry);

   // 2) STRICT MASTER: do not create any website-only transaction.\n\n   // 3) Re-read the Sheet so the website becomes exactly the same as Google Sheet.
   try{
     await syncFromGoogleSheet(false);
     if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
     if(typeof renderBankWiseView==="function"){
       const area=document.getElementById("bankWiseArea");
       if(area)renderBankWiseView();
     }
     setGoogleSyncStatus("Saved & synced ✓",true);
   }catch(syncErr){
     console.warn("Saved to Google Sheet but immediate re-sync failed:",syncErr);
     setGoogleSyncStatus("Saved to Google Sheet ✓ — dashboard already updated. Use Sync Now if needed.",true);
   }

 }catch(err){
   console.error(err);
   await syncFromGoogleSheet(false).catch(function(){});
   if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
   if(typeof renderBankWiseView==="function"){
     const area=document.getElementById("bankWiseArea");
     if(area)renderBankWiseView();
   }
   setGoogleSyncStatus("NOT SAVED — Google Sheet is master.",false);
   alert("Transaction NOT saved.\nNothing was added to the website because Google Sheet is the master.\n\n"+((err&&err.message)||err));
 }
}

function openTools(){document.getElementById("toolsModal").style.display="flex";renderTools()}
function closeTools(){document.getElementById("toolsModal").style.display="none"}
function saveConfig(){localStorage.setItem("moneyConfig",JSON.stringify(config))}
function renderTools(){
 let body="";
 Object.keys(config.categories).forEach(function(group){
  body+='<div class="tool-group"><h3>'+esc(group)+'</h3>';
  config.categories[group].forEach(function(item,i){
   body+='<div class="tool-row"><span>'+esc(item)+'</span><button class="remove" onclick="removeCategory(\''+esc(group)+'\','+i+')">Remove</button></div>';
  });
  body+='<div class="add-row"><input id="new_'+group+'" placeholder="Add sub category"><button onclick="addCategory(\''+esc(group)+'\')">＋ Add</button></div></div>';
 });
 body+='<div class="tool-group"><h3>Accounts</h3>';
 config.accounts.forEach(function(item,i){
  body+='<div class="tool-row"><span>'+esc(item)+'</span><button class="remove" onclick="removeAccount('+i+')">Remove</button></div>';
 });
 body+='<div class="add-row"><input id="new_account" placeholder="Add account"><button onclick="addAccount()">＋ Add</button></div></div>';
 document.getElementById("toolsBody").innerHTML=body;
}
function addCategory(group){
 let input=document.getElementById("new_"+group),v=input.value.trim();if(!v)return;
 if(!config.categories[group].includes(v))config.categories[group].push(v);
 saveConfig();renderTools();refreshManual();
}
function removeCategory(group,i){
 if(confirm("Remove this sub category? Existing saved data will not be deleted.")){config.categories[group].splice(i,1);saveConfig();renderTools();refreshManual()}
}
function addAccount(){
 let input=document.getElementById("new_account"),v=input.value.trim();if(!v)return;
 if(!config.accounts.includes(v))config.accounts.push(v);
 saveConfig();renderTools();refreshManual();
}
function removeAccount(i){
 if(confirm("Remove this account from future entries? Existing saved data will not be deleted.")){config.accounts.splice(i,1);saveConfig();renderTools();refreshManual()}
}
function refreshManual(){if(document.getElementById("moneyEntryArea").innerHTML.includes("Manual Data Entry")){manualEntry()}}


function clearAllMoneyData(){
  const overlay=document.getElementById("clearMoneyModal");
  if(overlay) overlay.style.display="flex";
}
function closeClearMoneyModal(){
  const overlay=document.getElementById("clearMoneyModal");
  if(overlay) overlay.style.display="none";
}
function confirmClearAllMoneyData(){
  try{
    // Remove every money-related key created by this tracker.
    const keys=[];
    for(let i=0;i<localStorage.length;i++) keys.push(localStorage.key(i));
    keys.filter(k=>k && k.toLowerCase().includes("money")).forEach(k=>localStorage.removeItem(k));

    // Re-create a clean empty transaction store.
    localStorage.setItem("moneyEntries","[]");

    // Reset editable category/account configuration back to defaults.
    config=JSON.parse(JSON.stringify(defaultConfig));

    // Reset all visible Money values immediately.
    [["moneyIncome","moneyIncomeCount"],["moneyExpenses","moneyExpenseCount"],["moneySavings","moneySavingsCount"],["moneyLoan","moneyLoanCount"]].forEach(function(p){
      const amount=document.getElementById(p[0]);
      const count=document.getElementById(p[1]);
      if(amount) amount.textContent="₹0.00";
      if(count) count.textContent="0 transactions";
    });

    const status=document.getElementById("moneyImportStatus");
    if(status) status.textContent="No sheet imported yet.";
    const table=document.getElementById("moneyTableWrap");
    if(table) table.innerHTML='<p class="muted">No transactions yet.</p>';
    const module=document.getElementById("moneyModule");
    if(module){ module.innerHTML=""; module.style.display="none"; }
    const tools=document.getElementById("toolsModal");
    if(tools) tools.style.display="none";

    updateMoneyDashboard();
    closeClearMoneyModal();

    const done=document.getElementById("clearDone");
    if(done){done.style.display="block";setTimeout(()=>done.style.display="none",3000);}
  }catch(err){
    const msg=document.getElementById("clearError");
    if(msg){msg.textContent="Could not clear data: "+err.message;msg.style.display="block";}
  }
}

function accountNameForEntry(x){
  const name=String(x.account||x.fromAccount||"").trim();
  return name || "Unassigned";
}

function calculateAccountBalances(){
  const balances={};

  // Process in true transaction order so a red H checkpoint resets only
  // that account from that exact point onward.
  moneySortChronological(moneyEntries()).forEach(function(x){
    const account=accountNameForEntry(x);
    if(!balances.hasOwnProperty(account)) balances[account]=0;

    const checkpointValue=sheetMoneyNumber(x.remainingAmountRaw);
    if(x.accountBalanceCheckpoint && checkpointValue!==null){
      // RED H RULE: confirmed account balance after this transaction.
      balances[account]=checkpointValue;
    }else{
      balances[account]+=cashEffectForEntry(x);
    }
  });

  return balances;
}

function currentAccountBalanceTotal(){
  const balances=calculateAccountBalances();
  return Object.keys(balances).reduce(function(sum,k){
    return sum+Number(balances[k]||0);
  },0);
}

function openAccountBalancePopup(){
  const modal=document.getElementById("accountBalanceModal");
  const list=document.getElementById("accountBalanceList");
  const totalBox=document.getElementById("accountBalanceTotal");
  if(!modal||!list||!totalBox)return;

  const balances=calculateAccountBalances();
  const rows=Object.entries(balances)
    .filter(function(r){return Math.abs(r[1])>0.000001;})
    .sort(function(a,b){return Math.abs(b[1])-Math.abs(a[1]);});

  const total=rows.reduce(function(sum,r){return sum+r[1];},0);
  const totalAbs=rows.reduce(function(sum,r){return sum+Math.abs(r[1]);},0)||1;
  const maxAbs=Math.max(1,...rows.map(function(r){return Math.abs(r[1]);}));

  totalBox.innerHTML=
    '<span>Total Remaining Balance</span>'+
    '<b>'+moneyFmt(total)+'</b>';

  if(!rows.length){
    list.innerHTML='<div class="money-empty-chart">No account balances available.</div>';
    modal.style.display="flex";
    return;
  }

  list.innerHTML=rows.map(function(r,i){
    const name=r[0],value=r[1];
    const width=Math.max(1,(Math.abs(value)/maxAbs)*100);
    const share=(Math.abs(value)/totalAbs*100).toFixed(1)+"%";
    const cls=value>=0?"positive":"negative";
    const barColor=value>=0?"#16a34a":"#ef4444";

    return '<div class="account-balance-row">'+
      '<div class="account-balance-name">'+esc(name)+'</div>'+
      '<div class="account-balance-value '+cls+'">'+moneyFmt(value)+'</div>'+
      '<div class="account-balance-share">'+share+'</div>'+
      '<div class="account-balance-bar"><span style="width:'+width+'%;background:'+barColor+'"></span></div>'+
    '</div>';
  }).join("");

  modal.style.display="flex";
}

function closeAccountBalancePopup(){
  const modal=document.getElementById("accountBalanceModal");
  if(modal)modal.style.display="none";
}

// ======================================================
// V160 — MONEY INSIGHTS + SAFE-TO-SPEND FORECAST
// ======================================================
let MI_budgetTargets={};
let MI_upcomingCommitments=[];

function MI_monthKey(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0");}
function MI_monthLabel(key){const p=String(key).split("-");return new Date(Number(p[0]),Number(p[1])-1,1).toLocaleDateString("en-US",{month:"long",year:"numeric"});}
function MI_entryMonth(x){const d=moneyReportingDate(x);return d?MI_monthKey(d):"";}
function MI_norm(v){return String(v||"").trim().toLowerCase();}
function MI_isSub(x,name){return MI_norm(x.subCategory)===MI_norm(name);}
function MI_sum(arr,fn){return arr.reduce(function(t,x){return t+(fn(x)||0);},0);}
function MI_pct(a,b){return b?((a/b)*100):0;}
function MI_escapeAttr(s){return esc(String(s||"")).replace(/"/g,"&quot;");}

function MI_monthStats(rows){
  let income=0,needs=0,wants=0,savings=0,savingsReturn=0,loanPaid=0,otherOut=0,totalIn=0,totalOut=0;
  const subs={};
  rows.forEach(function(x){
    const f=cashFlowBucketForEntry(x),a=amountNumber(x.amount),sub=String(x.subCategory||x.mainCategory||"Other").trim()||"Other";
    if(f==="Income")income+=a;
    if(f==="Needs"){needs+=a;subs[sub]=(subs[sub]||0)+a;}
    if(f==="Wants"){wants+=a;subs[sub]=(subs[sub]||0)+a;}
    if(f==="Savings")savings+=a;
    if(f==="Savings Return")savingsReturn+=a;
    if(f==="Loan Out" && MI_isSub(x,"Loan repayment paid"))loanPaid+=a;
    if(f==="Others"||f==="Out")otherOut+=a;
    const e=cashEffectForEntry(x);if(e>0)totalIn+=e;else totalOut+=Math.abs(e);
  });
  return {income,needs,wants,savings,savingsReturn,netSavings:savings-savingsReturn,loanPaid,otherOut,totalIn,totalOut,subs};
}

function MI_loanOutstanding(data){
  let took=0,gave=0;
  data.forEach(function(x){
    const a=amountNumber(x.amount),sub=MI_norm(x.subCategory),flow=cashFlowBucketForEntry(x);
    if(sub==="loan received")took+=a;
    else if(sub==="loan repayment paid")took-=a;
    else if(sub==="loan i gave" || (flow==="Loan Out" && sub==="money lent"))gave+=a;
    else if(sub==="loan repayment received")gave-=a;
  });
  return {took:Math.max(0,took),gave:Math.max(0,gave)};
}

function MI_currentAndPreviousKeys(data){
  const keys=data.map(MI_entryMonth).filter(Boolean).sort();
  const current=keys.length?keys[keys.length-1]:MI_monthKey(new Date());
  const p=current.split("-").map(Number),d=new Date(p[0],p[1]-2,1);
  return {current:current,previous:MI_monthKey(d)};
}

function MI_loadBudgets(){
  return new Promise(function(resolve){
    if(!(window.google&&google.script&&google.script.run)){MI_budgetTargets={};resolve({});return;}
    google.script.run.withSuccessHandler(function(r){MI_budgetTargets=(r&&r.success&&r.targets)||{};resolve(MI_budgetTargets);}).withFailureHandler(function(){MI_budgetTargets={};resolve({});}).MI_getBudgetTargetsForWeb();
  });
}
function MI_loadCommitments(){
  return new Promise(function(resolve){
    if(!(window.google&&google.script&&google.script.run)){MI_upcomingCommitments=[];resolve([]);return;}
    google.script.run.withSuccessHandler(function(r){MI_upcomingCommitments=(r&&r.success&&Array.isArray(r.commitments))?r.commitments:[];resolve(MI_upcomingCommitments);}).withFailureHandler(function(){MI_upcomingCommitments=[];resolve([]);}).MI_getUpcomingCommitmentsForWeb();
  });
}
function MI_monthShift(key,delta){const p=key.split('-').map(Number),d=new Date(p[0],p[1]-1+delta,1);return MI_monthKey(d);}
function MI_avg(vals){const a=vals.filter(v=>Number.isFinite(v));return a.length?a.reduce((s,v)=>s+v,0)/a.length:0;}
function MI_forecast(data,currentKey,cur,remaining){
  const hist=[];
  for(let i=1;i<=6;i++){const k=MI_monthShift(currentKey,-i),s=MI_monthStats(data.filter(x=>MI_entryMonth(x)===k));hist.push({key:k,stats:s});}
  const usable=hist.filter(x=>x.stats.totalIn||x.stats.totalOut||x.stats.needs||x.stats.savings);
  const recent=usable.slice(0,3);
  const base=recent.length?recent:usable;
  const avgNeeds=MI_avg(base.map(x=>x.stats.needs));
  const avgWants=MI_avg(base.map(x=>x.stats.wants));
  const avgSavings=MI_avg(base.map(x=>Math.max(0,x.stats.netSavings)));
  const avgLoan=MI_avg(base.map(x=>x.stats.loanPaid));
  const expectedRemainingNeeds=Math.max(0,avgNeeds-cur.needs);
  const expectedRemainingWants=Math.max(0,avgWants-cur.wants);
  const expectedRemainingSavings=Math.max(0,avgSavings-Math.max(0,cur.netSavings));
  const expectedRemainingLoan=Math.max(0,avgLoan-cur.loanPaid);
  const today=new Date(),p=currentKey.split('-').map(Number);
  const monthEnd=new Date(p[0],p[1],0);
  const commitments=MI_upcomingCommitments.filter(c=>{const d=parseTrackerDate(c.date);return d&&d>=new Date(p[0],p[1]-1,1)&&d<=monthEnd;});
  const commitmentTotal=MI_sum(commitments,c=>Number(c.amount||0));
  const safeForWants=remaining-expectedRemainingNeeds-expectedRemainingSavings-expectedRemainingLoan-commitmentTotal;
  const expectedMonthEnd=remaining-expectedRemainingNeeds-expectedRemainingWants-expectedRemainingSavings-expectedRemainingLoan-commitmentTotal;
  const confidence=base.length>=3?'Good':base.length>=2?'Fair':'Low';
  return {avgNeeds,avgWants,avgSavings,avgLoan,expectedRemainingNeeds,expectedRemainingWants,expectedRemainingSavings,expectedRemainingLoan,commitments,commitmentTotal,safeForWants,expectedMonthEnd,confidence,monthsUsed:base.length};
}

async function openViewMode6(){
  document.getElementById("viewModeChooser").style.display="none";
  document.getElementById("viewModeContent").innerHTML='<button class="secondary" onclick="backToViewOptions()">← Back</button><div class="view-section-title"><h2>💡 Money Insights</h2><p class="muted">Turn your transactions into decisions: where money goes, where spending increased, savings rate, loans, free cash and budget targets.</p></div><div id="moneyInsightsArea"><div class="muted">Building insights from Google Sheet transactions...</div></div>';
  await Promise.all([MI_loadBudgets(),MI_loadCommitments()]);
  MI_render();
}

function MI_render(){
  const host=document.getElementById("moneyInsightsArea");if(!host)return;
  const data=moneyEntries();
  if(!data.length){host.innerHTML='<div class="note">No money transactions available yet.</div>';return;}
  const kp=MI_currentAndPreviousKeys(data),curRows=data.filter(x=>MI_entryMonth(x)===kp.current),prevRows=data.filter(x=>MI_entryMonth(x)===kp.previous);
  const cur=MI_monthStats(curRows),prev=MI_monthStats(prevRows),loans=MI_loanOutstanding(data);
  const remaining=moneyLatestCumulativeBalance();
  const forecast=MI_forecast(data,kp.current,cur,remaining);
  const savingsRate=MI_pct(cur.netSavings,cur.totalIn);
  const essential=cur.needs+cur.loanPaid;
  const freeCash=cur.totalIn-cur.totalOut;
  const spendEntries=Object.entries(cur.subs).sort((a,b)=>b[1]-a[1]);
  const topSpend=spendEntries[0]||["No expense",0];

  let insights=[];
  if(prev.totalOut>0){const ch=cur.totalOut-prev.totalOut,p=MI_pct(Math.abs(ch),prev.totalOut);insights.push({t:ch>0?'Spending increased':'Spending reduced',v:(ch>0?'+':'−')+moneyFmt(Math.abs(ch))+' ('+p.toFixed(1)+'%) vs '+MI_monthLabel(kp.previous),c:ch>0?'mi-negative':'mi-positive'});}
  if(topSpend[1]>0)insights.push({t:'Largest Needs/Wants category',v:topSpend[0]+' · '+moneyFmt(topSpend[1]),c:'mi-neutral'});
  insights.push({t:'Savings rate',v:savingsRate.toFixed(1)+'% of this month total inflow',c:savingsRate>=20?'mi-positive':'mi-neutral'});
  if(loans.gave>0)insights.push({t:'Money still outside with others',v:'Loan I Gave outstanding '+moneyFmt(loans.gave),c:'mi-neutral'});
  if(loans.took>0)insights.push({t:'Loan still to repay',v:moneyFmt(loans.took),c:'mi-negative'});

  const budgetCats=Array.from(new Set(Object.keys(MI_budgetTargets).concat(spendEntries.map(x=>x[0])))).filter(Boolean).sort((a,b)=>a.localeCompare(b,undefined,{sensitivity:'base'}));
  let budgetRows=budgetCats.map(function(cat){
    const actual=cur.subs[cat]||0,target=Number(MI_budgetTargets[cat]||0),left=target?target-actual:0,pct=target?Math.min(100,actual/target*100):0;
    return '<div class="mi-row"><div><b>'+esc(cat)+'</b><div class="mi-bar"><span style="width:'+pct+'%"></span></div></div><div><small>Actual</small><b>'+moneyFmt(actual)+'</b></div><div><small>Target</small><input class="mi-budget-input" data-cat="'+MI_escapeAttr(cat)+'" type="number" min="0" step="1" value="'+(target||'')+'" placeholder="₹0"></div><div><small>'+(target?'Remaining':'Status')+'</small><b class="'+(target&&left<0?'mi-negative':'mi-positive')+'">'+(target?moneyFmt(left):'Set target')+'</b></div></div>';
  }).join('');

  host.innerHTML='<div class="mi-grid">'+
    '<div class="mi-card mi-good"><span>'+esc(MI_monthLabel(kp.current))+' Total In</span><b>'+moneyFmt(cur.totalIn)+'</b><small>All incoming cash</small></div>'+
    '<div class="mi-card mi-warn"><span>Total Out</span><b>'+moneyFmt(cur.totalOut)+'</b><small>All outgoing cash</small></div>'+
    '<div class="mi-card mi-blue"><span>Net Savings</span><b>'+moneyFmt(cur.netSavings)+'</b><small>'+savingsRate.toFixed(1)+'% savings rate</small></div>'+
    '<div class="mi-card '+(freeCash>=0?'mi-good':'mi-warn')+'"><span>Monthly Free Cash</span><b>'+moneyFmt(freeCash)+'</b><small>In − Out for this month</small></div>'+
    '<div class="mi-card mi-good"><span>Overall Remaining</span><b>'+moneyFmt(remaining)+'</b><small>Current cumulative cash balance</small></div>'+
    '<div class="mi-card '+(forecast.safeForWants>=0?'mi-good':'mi-warn')+'"><span>Safe for Wants</span><b>'+moneyFmt(forecast.safeForWants)+'</b><small>After forecast Needs, Savings, loans & commitments</small></div>'+
    '<div class="mi-card '+(forecast.expectedMonthEnd>=0?'mi-good':'mi-warn')+'"><span>Expected Month-End</span><b>'+moneyFmt(forecast.expectedMonthEnd)+'</b><small>After normal Needs + Wants pattern</small></div>'+
    '<div class="mi-card mi-purple"><span>Loan I Gave Outstanding</span><b>'+moneyFmt(loans.gave)+'</b><small>Still expected back</small></div>'+
    '<div class="mi-card mi-warn"><span>Loan I Took Outstanding</span><b>'+moneyFmt(loans.took)+'</b><small>Still to repay</small></div>'+
    '<div class="mi-card"><span>Essential + Loan Outflow</span><b>'+moneyFmt(essential)+'</b><small>Needs + loan repayment this month</small></div>'+
  '</div>'+
  '<div class="mi-subgrid"><div class="mi-section"><h3>🔎 What deserves attention</h3>'+insights.map(i=>'<div class="mi-insight"><strong>'+esc(i.t)+'</strong><span class="'+i.c+'">'+esc(i.v)+'</span></div>').join('')+'</div>'+
  '<div class="mi-section"><h3>📍 Where this month\'s spending went</h3>'+(spendEntries.length?spendEntries.slice(0,8).map(function(r){const pct=(cur.needs+cur.wants)?r[1]/(cur.needs+cur.wants)*100:0;return '<div class="mi-insight"><strong>'+esc(r[0])+'</strong><span>'+moneyFmt(r[1])+' · '+pct.toFixed(1)+'% of Needs/Wants</span></div>';}).join(''):'<div class="mi-empty">No Needs/Wants expenses this month.</div>')+'</div></div>'+
  '<div class="mi-section"><h3>🛡️ Safe-to-Spend Forecast</h3><p class="muted">Automatic forecast uses your recent 3 months first (up to 6 months when needed). It subtracts what you have already spent/saved this month, so it does not reserve the full monthly average again.</p>'+
    '<div class="mi-forecast-grid">'+
      '<div><span>Current available</span><b>'+moneyFmt(remaining)+'</b></div>'+
      '<div><span>Expected remaining Needs</span><b>− '+moneyFmt(forecast.expectedRemainingNeeds)+'</b></div>'+
      '<div><span>Expected remaining Savings</span><b>− '+moneyFmt(forecast.expectedRemainingSavings)+'</b></div>'+
      '<div><span>Expected loan payments</span><b>− '+moneyFmt(forecast.expectedRemainingLoan)+'</b></div>'+
      '<div><span>Upcoming commitments</span><b>− '+moneyFmt(forecast.commitmentTotal)+'</b></div>'+
      '<div class="mi-safe-result"><span>Safe for Wants</span><b>'+moneyFmt(forecast.safeForWants)+'</b></div>'+
    '</div><div class="mi-insight"><strong>Forecast confidence: '+forecast.confidence+'</strong><span>Based on '+forecast.monthsUsed+' completed month'+(forecast.monthsUsed===1?'':'s')+'. Normal Wants forecast: '+moneyFmt(forecast.avgWants)+' / month. Expected month-end after that pattern: '+moneyFmt(forecast.expectedMonthEnd)+'.</span></div></div>'+
  '<div class="mi-section"><h3>📅 Upcoming Commitments</h3><p class="muted">Optional only for exceptional future expenses that history cannot predict — insurance, trip, family function, major purchase, etc.</p><div class="mi-commit-form"><input id="miCommitDate" type="date"><input id="miCommitName" type="text" placeholder="e.g. Insurance"><input id="miCommitAmount" type="number" min="0" step="1" placeholder="Amount"><button class="primary" onclick="MI_addCommitment()">Add</button></div><div id="miCommitList">'+MI_commitmentHtml()+'</div><div id="miCommitStatus" class="muted" style="margin-top:8px"></div></div>'+
  '<div class="mi-section"><h3>🎯 Monthly Budget Targets — '+esc(MI_monthLabel(kp.current))+'</h3><p class="muted">Set a target for any expense sub category. Targets are saved in the Google Sheet, while Actual is calculated automatically from transactions.</p>'+(budgetRows||'<div class="mi-empty">Add Needs/Wants transactions to create budget categories.</div>')+'<div class="mi-actions"><button class="primary" onclick="MI_saveBudgets()">Save Budget Targets</button><button class="secondary" onclick="MI_render()">Refresh Insights</button></div><div id="miBudgetStatus" class="muted" style="margin-top:8px"></div></div>';
}

function MI_commitmentHtml(){
  if(!MI_upcomingCommitments.length)return '<div class="mi-empty">No exceptional upcoming commitments entered.</div>';
  return MI_upcomingCommitments.slice().sort((a,b)=>String(a.date).localeCompare(String(b.date))).map(function(c){return '<div class="mi-commit-row"><div><b>'+esc(c.name||'Commitment')+'</b><small>'+esc(c.date||'')+'</small></div><b>'+moneyFmt(Number(c.amount||0))+'</b><button class="secondary" onclick="MI_deleteCommitment(\''+esc(String(c.id||'')).replace(/'/g,"\\'")+'\')">Delete</button></div>';}).join('');
}
function MI_addCommitment(){
  const date=(document.getElementById('miCommitDate')||{}).value||'',name=((document.getElementById('miCommitName')||{}).value||'').trim(),amount=Number((document.getElementById('miCommitAmount')||{}).value||0),status=document.getElementById('miCommitStatus');
  if(!date||!name||!(amount>0)){if(status)status.textContent='Enter date, name and an amount above ₹0.';return;}
  if(status)status.textContent='Saving commitment...';
  google.script.run.withSuccessHandler(async function(r){MI_upcomingCommitments=(r&&r.commitments)||[];if(status)status.textContent='✓ Commitment saved.';MI_render();}).withFailureHandler(function(e){if(status)status.textContent='Save failed: '+((e&&e.message)||String(e));}).MI_saveUpcomingCommitmentForWeb({date:date,name:name,amount:amount});
}
function MI_deleteCommitment(id){
  google.script.run.withSuccessHandler(function(r){MI_upcomingCommitments=(r&&r.commitments)||[];MI_render();}).withFailureHandler(function(e){alert('Delete failed: '+((e&&e.message)||String(e)));}).MI_deleteUpcomingCommitmentForWeb(id);
}

function MI_saveBudgets(){
  const status=document.getElementById('miBudgetStatus');
  const targets={};document.querySelectorAll('.mi-budget-input').forEach(function(inp){const v=Number(inp.value||0);if(v>0)targets[inp.dataset.cat]=v;});
  if(status)status.textContent='Saving targets to Google Sheet...';
  if(!(window.google&&google.script&&google.script.run)){if(status)status.textContent='Google Apps Script is not available.';return;}
  google.script.run.withSuccessHandler(function(r){MI_budgetTargets=(r&&r.targets)||targets;if(status)status.textContent='✓ Budget targets saved.';MI_render();}).withFailureHandler(function(err){if(status)status.textContent='Save failed: '+((err&&err.message)||String(err));}).MI_saveBudgetTargetsForWeb(targets);
}

function moneyEntries(){return JSON.parse(localStorage.getItem("moneyEntries")||"[]")}
function moneyTotals(){
 const data=moneyEntries(), out={
   Income:[0,0],Expenses:[0,0],Savings:[0,0],
   LoanTook:[0,0],LoanGave:[0,0]
 };
 let savingsInvested=0;
 let savingsReturned=0;

 data.forEach(x=>{
   const flow=cashFlowBucketForEntry(x);
   const a=amountNumber(x.amount);
   const loanRel=loanRelationshipForEntry(x);

   if(flow==="Income"){
     out.Income[0]+=a; out.Income[1]++;
   }else if(flow==="Needs" || flow==="Wants"){
     out.Expenses[0]+=a; out.Expenses[1]++;
   }else if(flow==="Savings"){
     savingsInvested+=a;
     out.Savings[1]++;
   }else if(flow==="Savings Return"){
     savingsReturned+=a;
   }

   // Loan cards show OUTSTANDING balance, not gross cash movement.
   // Loan I Took = Loan received - Loan repayment paid.
   // Loan I Gave = Loan I Gave/Money lent - Loan repayment received.
   if(loanRel==="Loan I Took"){
     out.LoanTook[0]+=loanOutstandingEffect(x,"Loan I Took");
     out.LoanTook[1]++;
   }else if(loanRel==="Loan I Gave"){
     out.LoanGave[0]+=loanOutstandingEffect(x,"Loan I Gave");
     out.LoanGave[1]++;
   }
 });

 out.Savings[0]=savingsInvested-savingsReturned;
 out.SavingsInvested=savingsInvested;
 out.SavingsReturned=savingsReturned;
 out.TotalIn=moneyFlowTotals(data).totalIn;
 out.TotalOut=moneyFlowTotals(data).totalOut;
 out.Remaining=currentAccountBalanceTotal();
 return out;
}
function moneyFmt(n){return "₹"+Number(n||0).toLocaleString("en-IN",{minimumFractionDigits:2,maximumFractionDigits:2})}

function moneyMonthKey(d){
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0");
}
function moneyMonthLabel(key){
  const p=key.split("-");
  return new Date(Number(p[0]),Number(p[1])-1,1).toLocaleDateString("en-US",{month:"short"});
}
function moneyColorForIndex(i){
  const colors=["#16a34a","#2563eb","#f59e0b","#ef4444","#8b5cf6","#06b6d4","#ec4899","#64748b"];
  return colors[i%colors.length];
}

function renderMoneyVisuals(){
  const data=moneyEntries();

  // Transfer totals
  let transferIn=0, transferOut=0;
  data.forEach(function(x){
    const f=cashFlowBucketForEntry(x), a=amountNumber(x.amount);
    if(f==="In")transferIn+=a;
    if(f==="Out")transferOut+=a;
  });
  const ti=document.getElementById("moneyTransferIn");
  const to=document.getElementById("moneyTransferOut");
  if(ti)ti.textContent=moneyFmt(transferIn);
  if(to)to.textContent=moneyFmt(transferOut);

  const mt=moneyTotals();
  const loanInVisual=document.getElementById("moneyLoanInVisual");
  const loanOutVisual=document.getElementById("moneyLoanOutVisual");
  if(loanInVisual)loanInVisual.textContent=moneyFmt(mt.LoanTook[0]);
  if(loanOutVisual)loanOutVisual.textContent=moneyFmt(mt.LoanGave[0]);

  renderMoneyCashFlowChart(data);
  renderMoneyExpenseDonut(data);
  renderMoneyAllCategoryComparison(data);
  renderMoneySelectedCategoryTrend(data);
  renderMoneyAllSubCategoryTrends(data);
  renderMoneySavingsBars(data);
  renderMoneyRecentVisual(data);
}


let moneySelectedTrendCategory="Expenses";

function moneyAnalyticsBucket(x){
  const flow=cashFlowBucketForEntry(x);
  if(flow==="Income") return "Income";
  if(flow==="Needs") return "Needs";
  if(flow==="Wants") return "Wants";
  if(flow==="Savings" || flow==="Savings Return") return "Savings";
  if(flow==="In") return "In";
  if(flow==="Out") return "Out";
  if(flow==="Loan In") return "Loan In";
  if(flow==="Loan Out") return "Loan Out";
  return "Others";
}

function moneyAnalyticsAmount(x){
  const flow=cashFlowBucketForEntry(x);
  if(flow==="Savings Return") return savingsSignedAmount(x);
  return amountNumber(x.amount);
}

function moneyCategoryColor(name){
  const map={
    "Income":"#16a34a",
    "Expenses":"#ef4444",
    "Needs":"#f97316",
    "Wants":"#e11d48",
    "Savings":"#2563eb",
    "In":"#10b981",
    "Out":"#dc2626",
    "Loan In":"#0284c7",
    "Loan Out":"#c2410c",
    "Others":"#64748b"
  };
  return map[name]||"#64748b";
}

function buildMoneyAnalyticsTotals(data){
  const totals={
    "Income":0,
    "Expenses":0,
    "Needs":0,
    "Wants":0,
    "Savings":0,
    "In":0,
    "Out":0,
    "Loan In":0,
    "Loan Out":0,
    "Others":0
  };

  data.forEach(function(x){
    const flow=cashFlowBucketForEntry(x);
    const a=moneyAnalyticsAmount(x);

    if(flow==="Income"){
      totals.Income+=a;
    }else if(flow==="Needs"){
      totals.Needs+=a;
      totals.Expenses+=a;
    }else if(flow==="Wants"){
      totals.Wants+=a;
      totals.Expenses+=a;
    }else if(flow==="Savings" || flow==="Savings Return"){
      totals.Savings+=a;
    }else if(flow==="In"){
      totals.In+=a;
    }else if(flow==="Out"){
      totals.Out+=a;
    }else if(flow==="Loan In"){
      totals["Loan In"]+=a;
    }else if(flow==="Loan Out"){
      totals["Loan Out"]+=a;
    }else{
      totals.Others+=amountNumber(x.amount);
    }
  });

  return totals;
}

function renderMoneyAllCategoryComparison(data){
  const box=document.getElementById("moneyAllCategoryChart");
  const summary=document.getElementById("moneyHighLowSummary");
  if(!box||!summary)return;

  const totals=buildMoneyAnalyticsTotals(data);
  const order=["Income","Expenses","Savings","Needs","Wants","Loan In","Loan Out","Others"];
  const rows=order.map(function(name){return [name,totals[name]||0];});
  const max=Math.max(1,...rows.map(r=>Math.abs(r[1])));

  box.innerHTML=rows.map(function(r){
    const width=Math.max(1,(Math.abs(r[1])/max)*100);
    return '<div class="money-cat-row">'+
      '<div class="money-cat-label">'+esc(r[0])+'</div>'+
      '<div class="money-cat-track"><span style="width:'+width+'%;background:'+moneyCategoryColor(r[0])+'"></span></div>'+
      '<div class="money-cat-value">'+moneyFmt(r[1])+'</div>'+
    '</div>';
  }).join("");

  const meaningful=rows.filter(r=>Math.abs(r[1])>0);
  if(!meaningful.length){
    summary.innerHTML="";
    return;
  }

  const high=meaningful.slice().sort((a,b)=>Math.abs(b[1])-Math.abs(a[1]))[0];
  const low=meaningful.slice().sort((a,b)=>Math.abs(a[1])-Math.abs(b[1]))[0];

  summary.innerHTML=
    '<div class="money-high-low-card high">'+
      '<span>Highest total</span><b>'+esc(high[0])+'</b>'+
      '<small>'+moneyFmt(high[1])+'</small>'+
    '</div>'+
    '<div class="money-high-low-card low">'+
      '<span>Lowest non-zero total</span><b>'+esc(low[0])+'</b>'+
      '<small>'+moneyFmt(low[1])+'</small>'+
    '</div>';
}

function selectMoneyTrendCategory(name){
  moneySelectedTrendCategory=name;
  renderMoneySelectedCategoryTrend(moneyEntries());
}

function renderMoneySelectedCategoryTrend(data){
  const tabs=document.getElementById("moneyCategoryTrendTabs");
  const chart=document.getElementById("moneySelectedCategoryChart");
  const summary=document.getElementById("moneySelectedCategorySummary");
  if(!tabs||!chart||!summary)return;

  const categories=["Income","Expenses","Savings","Needs","Wants","Loan In","Loan Out","Others"];

  tabs.innerHTML=categories.map(function(name){
    return '<button class="money-trend-tab '+(moneySelectedTrendCategory===name?"active":"")+
      '" onclick="selectMoneyTrendCategory(\''+name.replace(/'/g,"\\'")+'\')">'+esc(name)+'</button>';
  }).join("");

  const grouped={};

  data.forEach(function(x){
    const d=moneyReportingDate(x);
    if(!d)return;

    const flow=cashFlowBucketForEntry(x);
    let include=false;
    let amount=amountNumber(x.amount);

    if(moneySelectedTrendCategory==="Income") include=flow==="Income";
    else if(moneySelectedTrendCategory==="Expenses") include=flow==="Needs"||flow==="Wants";
    else if(moneySelectedTrendCategory==="Savings"){
      include=flow==="Savings"||flow==="Savings Return";
      amount=moneyAnalyticsAmount(x);
    }
    else if(moneySelectedTrendCategory==="Needs") include=flow==="Needs";
    else if(moneySelectedTrendCategory==="Wants") include=flow==="Wants";
    else if(moneySelectedTrendCategory==="Loan In") include=flow==="Loan In";
    else if(moneySelectedTrendCategory==="Loan Out") include=flow==="Loan Out";
    else if(moneySelectedTrendCategory==="Others") include=moneyAnalyticsBucket(x)==="Others";

    if(!include)return;

    const key=moneyMonthKey(d);
    grouped[key]=(grouped[key]||0)+amount;
  });

  const keys=Object.keys(grouped).sort().slice(-12);

  if(!keys.length){
    summary.innerHTML="";
    chart.innerHTML='<div class="money-empty-chart">No data for '+esc(moneySelectedTrendCategory)+'</div>';
    return;
  }

  const values=keys.map(k=>grouped[k]);
  const highIndex=values.reduce((best,v,i,a)=>Math.abs(v)>Math.abs(a[best])?i:best,0);
  const nonZeroIndexes=values.map((v,i)=>[v,i]).filter(r=>Math.abs(r[0])>0);
  const lowIndex=nonZeroIndexes.length
    ? nonZeroIndexes.reduce((best,r)=>Math.abs(r[0])<Math.abs(values[best])?r[1]:best,nonZeroIndexes[0][1])
    : 0;
  const avg=values.reduce((s,v)=>s+v,0)/values.length;

  summary.innerHTML=
    '<div class="money-trend-stat"><span>Highest month</span><b>'+moneyMonthLabel(keys[highIndex])+' · '+moneyFmt(values[highIndex])+'</b></div>'+
    '<div class="money-trend-stat"><span>Lowest month</span><b>'+moneyMonthLabel(keys[lowIndex])+' · '+moneyFmt(values[lowIndex])+'</b></div>'+
    '<div class="money-trend-stat"><span>Monthly average</span><b>'+moneyFmt(avg)+'</b></div>';

  const max=Math.max(1,...values.map(v=>Math.abs(v)));
  const W=720,H=260,left=35,right=15,top=16,bottom=42;
  const chartW=W-left-right,chartH=H-top-bottom;
  const step=chartW/keys.length;
  const barW=Math.min(36,step*.55);
  const color=moneyCategoryColor(moneySelectedTrendCategory);

  let svg='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="none">';
  for(let i=0;i<=4;i++){
    const y=top+chartH*(i/4);
    svg+='<line x1="'+left+'" y1="'+y+'" x2="'+(W-right)+'" y2="'+y+'" stroke="#e8edf3" stroke-width="1"/>';
  }

  keys.forEach(function(k,i){
    const v=grouped[k];
    const h=chartH*(Math.abs(v)/max);
    const x=left+step*i+(step-barW)/2;
    const y=top+chartH-h;
    const isHigh=i===highIndex;
    const isLow=i===lowIndex;

    svg+='<rect x="'+x+'" y="'+y+'" width="'+barW+'" height="'+h+'" rx="5" fill="'+color+'" opacity="'+(isHigh?1:(isLow?0.55:0.78))+'"/>';
    if(isHigh){
      svg+='<text x="'+(x+barW/2)+'" y="'+Math.max(12,y-5)+'" text-anchor="middle" font-size="9" font-weight="700" fill="#15803d">HIGH</text>';
    }else if(isLow){
      svg+='<text x="'+(x+barW/2)+'" y="'+Math.max(12,y-5)+'" text-anchor="middle" font-size="9" font-weight="700" fill="#c2410c">LOW</text>';
    }
    svg+='<text x="'+(x+barW/2)+'" y="'+(H-14)+'" text-anchor="middle" font-size="10" fill="#64748b">'+moneyMonthLabel(k)+'</text>';
  });

  svg+='</svg>';
  chart.innerHTML=svg;
}

function renderMoneyCashFlowChart(data){
  const box=document.getElementById("moneyCashFlowChart");
  if(!box)return;

  const grouped={};
  data.forEach(function(x){
    const d=moneyReportingDate(x);
    if(!d)return;
    const key=moneyMonthKey(d);
    if(!grouped[key])grouped[key]={income:0,expense:0,savings:0};
    const flow=cashFlowBucketForEntry(x), a=amountNumber(x.amount);
    if(flow==="Income")grouped[key].income+=a;
    if(flow==="Needs"||flow==="Wants")grouped[key].expense+=a;
    if(flow==="Savings")grouped[key].savings+=a;
    if(flow==="Savings Return")grouped[key].savings-=a;
  });

  const keys=Object.keys(grouped).sort().slice(-6);
  if(!keys.length){
    box.innerHTML='<div class="money-empty-chart">No data yet</div>';
    return;
  }

  const max=Math.max(1,...keys.flatMap(k=>[grouped[k].income,grouped[k].expense,Math.abs(grouped[k].savings)]));
  const W=720,H=260,left=52,right=18,top=18,bottom=42;
  const chartW=W-left-right,chartH=H-top-bottom;
  const step=chartW/keys.length;
  const barW=Math.min(20,step*.19);

  let svg='<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="none">';
  for(let i=0;i<=4;i++){
    const y=top+chartH*(i/4);
    svg+='<line x1="'+left+'" y1="'+y+'" x2="'+(W-right)+'" y2="'+y+'" stroke="#e8edf3" stroke-width="1"/>';
  }

  keys.forEach(function(k,i){
    const x=left+step*i+step/2;
    const inc=grouped[k].income, exp=grouped[k].expense, sav=Math.max(0,grouped[k].savings);
    const ih=chartH*(inc/max), eh=chartH*(exp/max), sh=chartH*(sav/max);
    svg+='<rect x="'+(x-barW*1.5-3)+'" y="'+(top+chartH-ih)+'" width="'+barW+'" height="'+ih+'" rx="5" fill="#16a34a"/>';
    svg+='<rect x="'+(x-barW/2)+'" y="'+(top+chartH-eh)+'" width="'+barW+'" height="'+eh+'" rx="5" fill="#f97373"/>';
    svg+='<rect x="'+(x+barW/2+3)+'" y="'+(top+chartH-sh)+'" width="'+barW+'" height="'+sh+'" rx="5" fill="#2563eb"/>';
    svg+='<text x="'+x+'" y="'+(H-14)+'" text-anchor="middle" font-size="11" fill="#64748b">'+moneyMonthLabel(k)+'</text>';
  });

  svg+='</svg>';
  box.innerHTML=svg;
}

function renderMoneyExpenseDonut(data){
  const donut=document.getElementById("moneyExpenseDonut");
  const legend=document.getElementById("moneyExpenseLegend");
  const totalEl=document.getElementById("moneyDonutTotal");
  if(!donut||!legend)return;

  const groups={};
  data.forEach(function(x){
    const flow=cashFlowBucketForEntry(x);
    if(flow!=="Needs"&&flow!=="Wants")return;
    const sub=String(x.subCategory||"Other").trim()||"Other";
    groups[sub]=(groups[sub]||0)+amountNumber(x.amount);
  });

  const rows=Object.entries(groups).sort((a,b)=>b[1]-a[1]);
  const total=rows.reduce((s,r)=>s+r[1],0);
  if(totalEl)totalEl.textContent=moneyFmt(total);

  if(!rows.length){
    donut.style.background="#eef2f7";
    legend.innerHTML='<span class="muted">No expense data</span>';
    return;
  }

  const topRows=rows.slice(0,6);
  let acc=0, parts=[];
  topRows.forEach(function(r,i){
    const start=acc, pct=(r[1]/total)*100;
    acc+=pct;
    parts.push(moneyColorForIndex(i)+" "+start+"% "+acc+"%");
  });
  if(acc<100)parts.push("#e2e8f0 "+acc+"% 100%");
  donut.style.background="conic-gradient("+parts.join(",")+")";

  legend.innerHTML=topRows.map(function(r,i){
    const pct=total?((r[1]/total)*100).toFixed(1):"0.0";
    return '<div class="money-breakdown-row">'+
      '<span class="money-breakdown-name"><i style="background:'+moneyColorForIndex(i)+'"></i>'+esc(r[0])+'</span>'+
      '<span><b>'+moneyFmt(r[1])+'</b><small>'+pct+'%</small></span>'+
    '</div>';
  }).join("");
}



const moneySubCategoryIncluded = {
  "Income": true,
  "Expenses": true,
  "Savings": true,
  "Loan In": true,
  "Loan Out": true,
  "Others": true
};

function moneySubOverviewGroup(x){
  const flow=cashFlowBucketForEntry(x);

  if(flow==="Income") return "Income";
  if(flow==="Needs" || flow==="Wants") return "Expenses";
  if(flow==="Savings" || flow==="Savings Return") return "Savings";
  if(flow==="Loan In") return "Loan In";
  if(flow==="Loan Out") return "Loan Out";

  // In / Out are intentionally excluded completely.
  if(flow==="In" || flow==="Out") return "";

  return "Others";
}

function moneySubOverviewName(x){
  const group=moneySubOverviewGroup(x);
  if(group==="Savings") return savingsBaseSubCategory(x);
  return String(x.subCategory||"Uncategorized").trim() || "Uncategorized";
}

function moneySubOverviewAmount(x){
  const group=moneySubOverviewGroup(x);
  if(group==="Savings") return moneyAnalyticsAmount(x);
  return amountNumber(x.amount);
}

function moneySubOverviewColor(group){
  const colors={
    "Income":"#16a34a",
    "Expenses":"#ef4444",
    "Savings":"#f59e0b",
    "Loan In":"#7c3aed",
    "Loan Out":"#a16207",
    "Others":"#6b7280"
  };
  return colors[group] || "#64748b";
}

function toggleMoneySubCategoryGroup(group,checked){
  moneySubCategoryIncluded[group]=!!checked;
  renderMoneyAllSubCategoryTrends(moneyEntries());
}

function renderMoneyAllSubCategoryTrends(data){
  const checks=document.getElementById("moneySubCategoryFilterChecks");
  const bars=document.getElementById("moneySubCategoryOverallBars");
  const summary=document.getElementById("moneySubCategoryTotalsCards");
  const grand=document.getElementById("moneySubCategoryGrandTotal");
  if(!checks||!bars||!summary||!grand)return;

  const groups=["Income","Expenses","Savings","Loan In","Loan Out","Others"];

  checks.innerHTML=groups.map(function(group){
    const color=moneySubOverviewColor(group);
    const checked=moneySubCategoryIncluded[group] ? "checked" : "";
    const label=group==="Expenses" ? "Expenses (Needs + Wants)" : group;

    return '<label class="money-category-check">'+
      '<input type="checkbox" '+checked+
        ' onchange="toggleMoneySubCategoryGroup(\''+group.replace(/'/g,"\\'")+'\',this.checked)">'+
      '<span class="dot" style="background:'+color+'"></span>'+
      '<span>'+esc(label)+'</span>'+
    '</label>';
  }).join("");

  const rowsMap={};
  const groupTotals={};
  groups.forEach(function(g){groupTotals[g]=0;});

  data.forEach(function(x){
    const group=moneySubOverviewGroup(x);

    // Exclude transfers and unchecked groups.
    if(!group || !moneySubCategoryIncluded[group])return;

    const sub=moneySubOverviewName(x);
    const amount=moneySubOverviewAmount(x);

    // Keep same-named subcategories in different main groups separate internally.
    const key=group+"|||"+sub;

    if(!rowsMap[key]){
      rowsMap[key]={
        group:group,
        sub:sub,
        amount:0
      };
    }

    rowsMap[key].amount+=amount;
    groupTotals[group]+=amount;
  });

  const rows=Object.values(rowsMap)
    .filter(function(r){return Math.abs(r.amount)>0.000001;})
    .sort(function(a,b){return Math.abs(b.amount)-Math.abs(a.amount);});

  const totalAbs=rows.reduce(function(s,r){return s+Math.abs(r.amount);},0);
  const maxValue=Math.max(1,...rows.map(function(r){return Math.abs(r.amount);}));

  if(!rows.length){
    bars.innerHTML='<div class="money-empty-chart">No categories selected.</div>';
    summary.innerHTML="";
    grand.innerHTML="";
    return;
  }

  bars.innerHTML=rows.map(function(r){
    const color=moneySubOverviewColor(r.group);
    const width=Math.max(1,(Math.abs(r.amount)/maxValue)*100);
    const share=totalAbs ? (Math.abs(r.amount)/totalAbs*100).toFixed(1)+"%" : "0.0%";

    return '<div class="money-overall-sub-row">'+
      '<div class="money-overall-sub-label">'+
        '<span class="dot" style="background:'+color+'"></span>'+
        '<span class="money-overall-sub-name" title="'+esc(r.group+" · "+r.sub)+'">'+esc(r.sub)+'</span>'+
      '</div>'+
      '<div class="money-overall-sub-bar-area">'+
        '<div class="money-overall-sub-track"><span style="width:'+width+'%;background:'+color+'"></span></div>'+
        '<div class="money-overall-sub-value">'+moneyFmt(r.amount)+'</div>'+
      '</div>'+
      '<div class="money-overall-sub-share">'+share+'</div>'+
    '</div>';
  }).join("");

  const selectedGroups=groups.filter(function(g){return moneySubCategoryIncluded[g];});
  const selectedGrand=selectedGroups.reduce(function(s,g){return s+Math.abs(groupTotals[g]||0);},0);

  summary.innerHTML=selectedGroups.map(function(group){
    const value=groupTotals[group]||0;
    const pct=selectedGrand ? (Math.abs(value)/selectedGrand*100).toFixed(1) : "0.0";
    const label=group==="Expenses" ? "Total Expenses" : "Total "+group;
    const color=moneySubOverviewColor(group);

    return '<div class="money-sub-summary-card" style="border-color:'+color+'55">'+
      '<span>'+esc(label)+'</span>'+
      '<b>'+moneyFmt(value)+'</b>'+
      '<small style="color:'+color+'">'+pct+'%</small>'+
    '</div>';
  }).join("");

  grand.innerHTML=
    '<span>Total Overall (selected categories)</span>'+
    '<b>'+moneyFmt(selectedGrand)+'</b>';
}


function renderMoneySavingsBars(data){
  const box=document.getElementById("moneySavingsBars");
  if(!box)return;

  const groups={};
  data.forEach(function(x){
    const flow=cashFlowBucketForEntry(x);
    if(flow!=="Savings" && flow!=="Savings Return")return;
    const sub=savingsBaseSubCategory(x);
    groups[sub]=(groups[sub]||0)+savingsSignedAmount(x);
  });

  const rows=Object.entries(groups).sort((a,b)=>b[1]-a[1]);
  const positiveRows=rows.map(r=>[r[0],Math.max(0,r[1])]);
  const total=positiveRows.reduce((s,r)=>s+r[1],0);

  if(!rows.length){
    box.innerHTML='<p class="muted">No savings data yet.</p>';
    return;
  }

  box.innerHTML=rows.slice(0,6).map(function(r,i){
    const display=Math.max(0,r[1]);
    const pct=total?Math.max(2,(display/total)*100):0;
    return '<div class="money-progress-row">'+
      '<div class="money-progress-top"><span>'+esc(r[0])+'</span><b>'+moneyFmt(r[1])+'</b></div>'+
      '<div class="money-progress-track"><span style="width:'+pct+'%;background:'+moneyColorForIndex(i+1)+'"></span></div>'+
    '</div>';
  }).join("");
}

function renderMoneyRecentVisual(data){
  const box=document.getElementById("moneyRecentVisual");
  if(!box)return;

  const rows=data.slice().sort(function(a,b){
    const da=parseTrackerDate(a.date),db=parseTrackerDate(b.date);
    return (db?db.getTime():0)-(da?da.getTime():0);
  }).slice(0,7);

  if(!rows.length){
    box.innerHTML='<p class="muted">No transactions yet.</p>';
    return;
  }

  box.innerHTML='<div class="money-recent-table">'+rows.map(function(x){
    const flow=cashFlowBucketForEntry(x);
    const positive=(flow==="Income"||flow==="In"||flow==="Loan In"||flow==="Savings Return");
    return '<div class="money-recent-row">'+
      '<div><b>'+esc(x.subCategory||x.mainCategory||"Transaction")+'</b><span>'+displayTrackerDate(x.date)+' · '+esc(x.account||x.fromAccount||"")+'</span></div>'+
      '<strong class="'+(positive?"positive":"negative")+'">'+(positive?"+":"−")+moneyFmt(x.amount).replace("₹","₹")+'</strong>'+
    '</div>';
  }).join("")+'</div>';
}

function updateMoneyDashboard(){
 const t=moneyTotals();
 [["Income","moneyIncome","moneyIncomeCount"],["Expenses","moneyExpenses","moneyExpenseCount"],["Savings","moneySavings","moneySavingsCount"],["LoanTook","moneyLoanTook","moneyLoanTookCount"],["LoanGave","moneyLoanGave","moneyLoanGaveCount"]].forEach(x=>{
   const [g,val,count]=x;const e=document.getElementById(val),c=document.getElementById(count);
   if(e)e.textContent=moneyFmt(t[g][0]);if(c)c.textContent=t[g][1]+" transactions";
 });
 const rem=document.getElementById("moneyRemaining");
 if(rem)rem.textContent=moneyFmt(t.Remaining);
 renderMoneyVisuals();
 const data=moneyEntries();
 const status=document.getElementById("moneyImportStatus");
 const table=document.getElementById("moneyTableWrap");
 if(!status||!table)return;
 const sheetCount=data.filter(x=>x.source==="sheet"||x.source==="google-sheet").length;
 status.textContent=sheetCount?("✓ "+sheetCount+" sheet transactions loaded. Income/Expenses/Savings are calculated from your master categories and Amount Category. Uploading another sheet replaces the previous sheet import. Manual entries are retained."):"No sheet imported yet.";
 const recent=data.slice(-100).reverse();
 table.innerHTML=recent.length?'<div style="overflow:auto"><table style="width:100%;border-collapse:collapse;font-size:13px"><thead><tr>'+
 '<th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Date</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Main Category</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Sub Category</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Explanation</th><th style="text-align:right;padding:8px;border-bottom:1px solid #ddd">Amount</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Account</th></tr></thead><tbody>'+
 recent.map(x=>'<tr><td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.date||"")+'</td><td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.mainCategory||"")+'</td><td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.subCategory||"")+'</td><td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.explanation||"")+'</td><td style="padding:8px;border-bottom:1px solid #eee;text-align:right">'+moneyFmt(x.amount)+'</td><td style="padding:8px;border-bottom:1px solid #eee">'+esc(x.account||x.fromAccount||"")+'</td></tr>').join("")+
 '</tbody></table></div>':'<p class="muted">No transactions yet.</p>';
}
function toggleTimeForm(){
 let f=document.getElementById("timeForm");f.style.display=f.style.display==="none"?"block":"none";
 if(f.style.display==="block"&&!document.getElementById("tStart").value){
  let d=new Date();document.getElementById("tStart").value=d.toTimeString().slice(0,5);
 }
}
function minutes(t){let a=t.split(":").map(Number);return a[0]*60+a[1]}
function isCurrent(b){
 let d=new Date(),now=d.getHours()*60+d.getMinutes(),a=minutes(b.start),z=minutes(b.end);
 return a<=z?now>=a&&now<z:now>=a||now<z;
}
function saveTimeBlock(){
 let b={id:Date.now(),desc:document.getElementById("tDesc").value.trim(),start:document.getElementById("tStart").value,end:document.getElementById("tEnd").value,cat:document.getElementById("tCat").value,priority:document.getElementById("tPriority").value,tasks:document.getElementById("tTasks").value};
 if(!b.desc||!b.start||!b.end){alert("Please enter description, start and end time.");return}
 timeBlocks.push(b);localStorage.setItem("timeBlocks",JSON.stringify(timeBlocks));
 document.getElementById("tDesc").value="";document.getElementById("tTasks").value="";toggleTimeForm();renderSchedule();
}
function deleteTimeBlock(id){timeBlocks=timeBlocks.filter(x=>x.id!==id);localStorage.setItem("timeBlocks",JSON.stringify(timeBlocks));renderSchedule()}
function renderSchedule(){
 let arr=[...timeBlocks].sort((a,b)=>minutes(a.start)-minutes(b.start));
 document.getElementById("schedule").innerHTML=arr.length?arr.map(b=>'<div class="time-block '+(isCurrent(b)?"current":"")+'"><div><b>'+esc(b.start)+' – '+esc(b.end)+'</b><br>'+esc(b.desc)+'<br><span class="muted">'+esc(b.cat)+' · '+esc(b.priority)+' priority</span>'+(b.tasks?'<br><small>'+esc(b.tasks)+'</small>':"")+'</div><button class="delete" onclick="deleteTimeBlock('+b.id+')">Delete</button></div>').join(""):'<p class="muted">No time blocks yet.</p>';
}
function updateCountdown(){
 let now=new Date(),end=new Date(now);end.setHours(24,0,0,0);let s=Math.max(0,Math.floor((end-now)/1000));
 let h=Math.floor(s/3600),m=Math.floor((s%3600)/60),sec=s%60;
 document.getElementById("countdown").textContent=String(h).padStart(2,"0")+"h "+String(m).padStart(2,"0")+"m "+String(sec).padStart(2,"0")+"s";
}
updateCountdown();renderSchedule();updateMoneyDashboard();setInterval(updateCountdown,1000);setInterval(renderSchedule,30000);


document.addEventListener("DOMContentLoaded",function(){
  const startButton=document.querySelector(".visual-start");
  if(startButton){
    startButton.addEventListener("click",function(){
      startApp();
    });
  }
});
function TB_closeStatusDetails(){
  const modal=document.getElementById("tbStatusDetailsModal");
  if(modal){
    modal.style.display="none";
    modal.classList.remove("open");
  }
  document.body.style.overflow="";
}


function TB_materializeProjectedTask(recurringId,dateKey,status){
  TB_syncRecurringOccurrencesForDate(dateKey);
  const tasks=TB_loadTasks();
  const t=tasks.find(function(x){return x.source==="recurring"&&x.recurringId===recurringId&&x.planDate===dateKey});
  if(!t)return;
  t.status=status;
  if(typeof TB_setStatusTimestamp==="function")TB_setStatusTimestamp(t,status);
  TB_saveTasks(tasks);
  TB_renderStatusDashboard();
  TB_openStatusDetails(status);
}
function TB_openStatusDetails(status){
  const modal=document.getElementById("tbStatusDetailsModal"),
        title=document.getElementById("tbStatusDetailsTitle"),
        sub=document.getElementById("tbStatusDetailsSubtitle"),
        summary=document.getElementById("tbStatusDetailsSummary"),
        table=document.getElementById("tbStatusDetailsTable");
  if(!modal||!title||!sub||!summary||!table)return;

  const tasks=TB_tasksForStatusDashboard(status);
  const label={Today:"Today",Week:"This Week",Month:"This Month",Year:"This Year",Overall:"Overall"}[TB_statusPeriod];

  title.textContent="📌 "+status+" Tasks — "+label;
  sub.textContent=tasks.length+" task"+(tasks.length===1?"":"s")+" · actual tasks are editable";

  const planned=tasks.reduce(function(s,t){return s+(Number(t.estimate)||0)},0);
  const focused=tasks.reduce(function(s,t){return s+(Number(t.actualMinutes)||0)},0);
  const wp=tasks.filter(function(t){return Number(t.priority)>0}).length;
  summary.innerHTML='<div><span>Tasks</span><b>'+tasks.length+'</b></div>'+
    '<div><span>Planned time</span><b>'+HL_fmtMinutes(planned)+'</b></div>'+
    '<div><span>Focused time</span><b>'+HL_fmtMinutes(focused)+'</b></div>'+
    '<div><span>With priority</span><b>'+wp+'</b></div>';

  const projectedCount=tasks.filter(function(t){return t.projected}).length;
  const note=projectedCount?'<div class="tb-projection-note">'+projectedCount+' future recurring occurrence'+(projectedCount===1?"":"s")+' included in this period.</div>':'';

  if(!tasks.length){
    table.innerHTML=note+'<div class="tb-empty">No '+esc(status)+' tasks.</div>';
    modal.style.display="flex";return;
  }

  const rows=tasks.slice().sort(function(a,b){
    if(String(a.planDate)!==String(b.planDate))return String(a.planDate).localeCompare(String(b.planDate));
    return String(a.startTime||"").localeCompare(String(b.startTime||""));
  }).map(function(t){
    const mins=Math.max(1,Number(t.estimate)||20);
    const end=t.startTime?TB_addMinutesToTime(t.startTime,mins):"—";
    const source=t.projected?"Recurring · "+(t.recurringKind||""):t.source==="recurring"?"Recurring · "+(t.recurringKind||""):"Brain / Manual";

    if(t.projected){
      return '<tr><td><b>'+esc(t.title)+'</b></td><td>#</td><td>'+esc(t.type)+'</td><td>'+esc(t.startTime||"")+'</td><td>'+mins+'</td><td>'+end+'</td><td>'+esc(t.planDate)+'</td><td>Not Started</td>'+
        '<td><button type="button" class="start" onclick="TB_materializeProjectedTask(\''+t.recurringId+'\',\''+t.planDate+'\',\'In Progress\')">Start</button> '+
        '<button type="button" class="done" onclick="TB_materializeProjectedTask(\''+t.recurringId+'\',\''+t.planDate+'\',\'Done\')">Done</button> '+
        '<button type="button" class="hold" onclick="TB_materializeProjectedTask(\''+t.recurringId+'\',\''+t.planDate+'\',\'Hold\')">Hold</button></td>'+
        '<td><span class="tb-source-pill recurring">'+esc(source)+'</span></td></tr>';
    }

    return '<tr><td><input class="tb-inline-task" value="'+esc(t.title||"")+'" onchange="TB_inlineEditTask(\''+t.id+'\',\'title\',this.value)"></td>'+
      '<td><input class="tb-inline-priority" type="number" min="1" value="'+esc(t.priority||"")+'" placeholder="#" onchange="TB_inlineEditTask(\''+t.id+'\',\'priority\',this.value)"></td>'+
      '<td><select onchange="TB_inlineEditTask(\''+t.id+'\',\'type\',this.value)">'+["Job","Personal","Money","Health","Learning","Other"].map(function(x){return '<option '+(t.type===x?"selected":"")+'>'+x+'</option>'}).join("")+'</select></td>'+
      '<td><input type="time" value="'+esc(t.startTime||"")+'" onchange="TB_inlineEditTask(\''+t.id+'\',\'startTime\',this.value)"></td>'+
      '<td><input type="number" min="1" value="'+mins+'" onchange="TB_inlineEditTask(\''+t.id+'\',\'estimate\',this.value)"></td>'+
      '<td>'+end+'</td><td><input type="date" value="'+esc(t.planDate||TB_todayKey())+'" onchange="TB_inlineEditTask(\''+t.id+'\',\'planDate\',this.value)"></td>'+
      '<td><select onchange="TB_inlineEditTask(\''+t.id+'\',\'status\',this.value)">'+["Not Started","In Progress","Done","Hold"].map(function(x){return '<option '+(t.status===x?"selected":"")+'>'+x+'</option>'}).join("")+'</select></td>'+
      '<td class="tb-inline-actions"><button type="button" class="start" onclick="TB_actionFromPopup(this,\''+t.id+'\',\'In Progress\')">Start</button>'+
      '<button type="button" class="done" onclick="TB_actionFromPopup(this,\''+t.id+'\',\'Done\')">Done</button>'+
      '<button type="button" class="hold" onclick="TB_actionFromPopup(this,\''+t.id+'\',\'Hold\')">Hold</button>'+
      '<button type="button" class="delete" onclick="TB_deleteFromPopup(this,\''+t.id+'\')">Delete</button></td>'+
      '<td><span class="tb-source-pill '+(t.source==="recurring"?"recurring":"")+'">'+esc(source)+'</span></td></tr>';
  }).join("");

  table.innerHTML=note+'<table><thead><tr><th>Task</th><th>P</th><th>Type</th><th>Start</th><th>Min</th><th>End</th><th>Date</th><th>Status</th><th>Action</th><th>Source</th></tr></thead><tbody>'+rows+'</tbody></table>';
  modal.style.display="flex";
}








/* ============================================================
   V100 REVIEW — SYNCED, FILTERED, EDITABLE
   ============================================================ */
function RV_monthNames(){
  return ["January","February","March","April","May","June","July","August","September","October","November","December"];
}
function RV_initSelectors(){
  const m=document.getElementById("rvMonth"),y=document.getElementById("rvYear");
  if(!m||!y)return;
  if(!m.options.length){
    RV_monthNames().forEach(function(name,i){
      const o=document.createElement("option");o.value=i;o.textContent=name;m.appendChild(o);
    });
  }
  if(!y.options.length){
    const now=new Date();
    for(let yr=now.getFullYear()-7;yr<=now.getFullYear()+5;yr++){
      const o=document.createElement("option");o.value=yr;o.textContent=yr;y.appendChild(o);
    }
  }
  if(m.dataset.ready!=="1"){
    const now=new Date();
    m.value=now.getMonth();y.value=now.getFullYear();m.dataset.ready="1";
  }
}
function RV_selectedYM(){
  RV_initSelectors();
  return {month:Number(document.getElementById("rvMonth").value),year:Number(document.getElementById("rvYear").value)};
}
function RV_changeMonth(delta){
  const x=RV_selectedYM(),d=new Date(x.year,x.month+delta,1);
  document.getElementById("rvMonth").value=d.getMonth();
  document.getElementById("rvYear").value=d.getFullYear();
  RV_renderAll();
}
function RV_goCurrentMonth(){
  const n=new Date();RV_initSelectors();
  document.getElementById("rvMonth").value=n.getMonth();
  document.getElementById("rvYear").value=n.getFullYear();
  RV_renderAll();
}
function RV_scrollCalendar(){
  const x=document.getElementById("rvCalendarCard");
  if(x)x.scrollIntoView({behavior:"smooth",block:"start"});
}
function RV_key(d){
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
}
function RV_rupee(n){
  return "₹"+Number(n||0).toLocaleString("en-IN",{maximumFractionDigits:2});
}
function RV_parseMoneyDate(v){
  if(!v)return null;
  if(typeof parseTrackerDate==="function"){
    const d=parseTrackerDate(v);if(d)return d;
  }
  if(v instanceof Date)return v;
  const s=String(v).trim();
  let m=s.match(/^(\d{1,2})[-\/](\d{1,2})[-\/](\d{4})$/);
  if(m)return new Date(Number(m[3]),Number(m[2])-1,Number(m[1]));
  m=s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if(m)return new Date(Number(m[1]),Number(m[2])-1,Number(m[3]));
  return null;
}

/* -------- MONEY — use the exact same money store and flow classification -------- */
function RV_moneyRows(){
  return (typeof moneyEntries==="function" ? moneyEntries() : []).filter(function(x){
    return x && x.date && x.mainCategory && Number(x.amount||0)!==0;
  });
}
function RV_moneyForDate(key){
  const rows=RV_moneyRows();
  let totalIn=0,totalOut=0,income=0,expense=0,saving=0,txCount=0;
  rows.forEach(function(r){
    const d=RV_parseMoneyDate(r.date);
    if(!d || RV_key(d)!==key)return;
    const a=typeof amountNumber==="function"?amountNumber(r.amount):(Number(r.amount)||0);
    const flow=typeof cashFlowBucketForEntry==="function"?cashFlowBucketForEntry(r):String(r.mainCategory||"").trim();
    txCount++;
    if(flow==="Income"||flow==="In"||flow==="Loan In"||flow==="Savings Return")totalIn+=a;
    if(flow==="Needs"||flow==="Wants"||flow==="Savings"||flow==="Out"||flow==="Others"||flow==="Loan Out")totalOut+=a;
    if(flow==="Income")income+=a;
    if(flow==="Needs"||flow==="Wants")expense+=a;
    if(flow==="Savings")saving+=a;
  });
  const target=RV_parseMoneyDate(key);
  const overallRemaining=target&&typeof moneyCumulativeBalanceAt==="function"?moneyCumulativeBalanceAt(target):0;
  return {income,expense,saving,totalIn,totalOut,netMovement:totalIn-totalOut,overallRemaining,txCount};
}

/* -------- HEALTH — exact Health stores -------- */
function RV_healthForDate(key){
  let calories=0,sleepMinutes=0,weight=null;
  try{
    const foods=typeof HL_foods==="function"?HL_foods():JSON.parse(localStorage.getItem("healthFoodsV1")||"[]");
    calories=foods.filter(x=>x.date===key).reduce((s,x)=>s+(Number(x.calories)||0),0);
  }catch(e){}
  try{
    const sleeps=typeof HL_sleeps==="function"?HL_sleeps():JSON.parse(localStorage.getItem("healthSleepV1")||"[]");
    const s=sleeps.find(x=>x.date===key);
    if(s)sleepMinutes=Number(s.minutes)||0;
  }catch(e){}
  try{
    const weights=typeof HL_weights==="function"?HL_weights():JSON.parse(localStorage.getItem("healthWeightsV1")||"[]");
    const same=weights.filter(x=>x.date===key);
    if(same.length)weight=Number(same[same.length-1].weight);
  }catch(e){}
  return {calories:calories,sleepMinutes:sleepMinutes,weight:weight};
}

/* -------- TASKS — exact Time task store -------- */
function RV_tasksForDate(key){
  let all=[];try{all=typeof TB_loadTasks==="function"?TB_loadTasks():[]}catch(e){}
  const rows=all.filter(t=>t.planDate===key||t.completedDate===key);
  return {
    rows:rows,
    done:rows.filter(t=>t.status==="Done"||t.completedDate===key).length,
    notStarted:rows.filter(t=>t.status==="Not Started"&&t.planDate===key).length,
    inProgress:rows.filter(t=>t.status==="In Progress"&&t.planDate===key).length,
    hold:rows.filter(t=>t.status==="Hold"&&t.planDate===key).length,
    total:rows.length
  };
}
function RV_dayData(key){
  return {key:key,money:RV_moneyForDate(key),health:RV_healthForDate(key),tasks:RV_tasksForDate(key)};
}
function RV_monthData(){
  const x=RV_selectedYM(),last=new Date(x.year,x.month+1,0).getDate(),out=[];
  for(let d=1;d<=last;d++)out.push(RV_dayData(RV_key(new Date(x.year,x.month,d))));
  return out;
}

function RV_metricLabel(metric){
  return {
    all:"Overall — all tracked information",
    income:"Money — all daily transactions",
    expense:"Expenses — Needs + Wants spending",
    saving:"Savings — invested minus savings returns",
    sleep:"Sleep — recorded sleep duration",
    done:"Tasks Done — completed work",
    pending:"Not Started — pending tasks",
    calories:"Calories — recorded food calories",
    weight:"Weight — recorded weight"
  }[metric]||"Overall";
}
function RV_selectMetric(metric,el){
  RV_selectedMetric=metric||"all";

  document.querySelectorAll("[data-rv-metric]").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll("[data-rv-filter]").forEach(x=>x.classList.remove("active"));

  document.querySelectorAll('[data-rv-metric="'+RV_selectedMetric+'"]').forEach(x=>x.classList.add("active"));
  document.querySelectorAll('[data-rv-filter="'+RV_selectedMetric+'"]').forEach(x=>x.classList.add("active"));

  const text=document.getElementById("rvMetricViewText");
  if(text)text.textContent=RV_metricLabel(RV_selectedMetric);

  RV_renderCalendar(RV_monthData());
  RV_scrollCalendar();
}
function RV_hasMetric(d,metric){
  if(metric==="income") return !!(d.money && d.money.txCount>0);
  if(metric==="expense") return !!(d.money && d.money.totalOut>0);
  if(metric==="saving") return !!(d.money && d.money.saving>0);
  if(metric==="sleep") return !!(d.health && d.health.sleepMinutes);
  if(metric==="done") return !!(d.tasks && d.tasks.done);
  if(metric==="pending") return !!(d.tasks && d.tasks.pending);
  if(metric==="calories") return !!(d.health && d.health.calories);
  if(metric==="weight") return !!(d.health && d.health.weight!=null);
  if(metric==="all") return !!(
    (d.money && d.money.txCount>0) ||
    (d.health && (d.health.sleepMinutes||d.health.calories||d.health.weight!=null)) ||
    (d.tasks && d.tasks.total)
  );
  return false;
}
function RV_metricMissingText(metric){
  return {
    income:"No money transaction entered",
    expense:"No expense entered",
    saving:"No savings entered",
    sleep:"No sleep entered",
    done:"No completed task",
    pending:"No not-started task",
    calories:"No calories entered",
    weight:"No weight entered",
    all:"No information entered"
  }[metric]||"Missing data";
}
function RV_metricLine(d,metric){
  if(metric==="income")return d.money.txCount?
    '<span class="rv-money-income">💵 Income '+RV_rupee(d.money.totalIn||0)+'</span>'+
    '<span class="rv-money-expense">💸 Expenses '+RV_rupee(d.money.totalOut||0)+'</span>'+
    '<span class="rv-money-saving">🏦 Savings '+RV_rupee(d.money.saving||0)+'</span>'+
    '<span class="rv-money-remaining">💰 Remaining '+RV_rupee(d.money.overallRemaining||0)+'</span>':"";
  if(metric==="expense")return d.money.expense?'<span class="bad">💸 Expense '+RV_rupee(d.money.expense)+'</span>':"";
  if(metric==="saving")return d.money.saving?'<span class="neutral">🏦 Savings '+RV_rupee(d.money.saving)+'</span>':"";
  if(metric==="sleep")return d.health.sleepMinutes?'<span>😴 Sleep '+HL_fmtMinutes(d.health.sleepMinutes)+'</span>':"";
  if(metric==="done")return d.tasks.done?'<span class="good">✅ Done '+d.tasks.done+'</span>':"";
  if(metric==="pending")return d.tasks.notStarted?'<span class="pending">📌 Not Started '+d.tasks.notStarted+'</span>':"";
  if(metric==="calories")return d.health.calories?'<span>🍽️ '+Math.round(d.health.calories)+' kcal</span>':"";
  if(metric==="weight")return d.health.weight!=null?'<span>⚖️ '+d.health.weight.toFixed(1)+' kg</span>':"";
  return "";
}

function RV_habitOccurrence(rule,dateKey){
  const tasks=typeof TB_loadTasks==="function"?TB_loadTasks():[];
  return tasks.find(function(t){return t.source==="recurring"&&t.recurringId===rule.id&&t.planDate===dateKey;})||null;
}
function RV_habitSetDone(recurringId,dateKey,checked){
  if(typeof TB_syncRecurringOccurrencesForDate==="function")TB_syncRecurringOccurrencesForDate(dateKey);
  const tasks=typeof TB_loadTasks==="function"?TB_loadTasks():[];
  const task=tasks.find(function(t){return t.source==="recurring"&&t.recurringId===recurringId&&t.planDate===dateKey;});
  if(!task)return;
  const status=checked?"Done":"Not Started";
  task.status=status;
  if(typeof TB_setStatusTimestamp==="function")TB_setStatusTimestamp(task,status);
  if(checked)task.completedDate=dateKey;
  if(typeof TB_saveTasks==="function")TB_saveTasks(tasks);
  RV_renderAll();
}
function RV_renderHabitTracker(){
  const host=document.getElementById("rvHabitTracker");
  const summary=document.getElementById("rvHabitSummary");
  if(!host)return;

  const x=RV_selectedYM();
  const rules=(typeof TB_loadRecurring==="function"?TB_loadRecurring():[])
    .filter(function(r){return r&&r.active!==false;});

  if(!rules.length){
    host.innerHTML='<p class="muted">No active recurring tasks. Add them in Time → Recurring.</p>';
    if(summary)summary.textContent="0 habits";
    return;
  }

  const lastDay=new Date(x.year,x.month+1,0).getDate();
  const monthName=new Date(x.year,x.month,1).toLocaleDateString("en-IN",{month:"long"});
  const todayKey=RV_key(new Date());
  let total=0,doneTotal=0;

  const headDays=Array.from({length:lastDay},function(_,i){
    const key=RV_key(new Date(x.year,x.month,i+1));
    return '<th class="'+(key===todayKey?'jh-today':'')+'">'+(i+1)+'</th>';
  }).join("");

  const body=rules.map(function(rule){
    let ruleTotal=0,ruleDone=0;
    const cells=[];

    for(let day=1;day<=lastDay;day++){
      const key=RV_key(new Date(x.year,x.month,day));
      const matches=typeof TB_recurringMatchesDate==="function"
        ? TB_recurringMatchesDate(rule,key)
        : true;
      const deleted=typeof TB_isRecurringOccurrenceDeleted==="function"
        ? TB_isRecurringOccurrenceDeleted(key,rule.id)
        : false;

      if(!matches||deleted){
        cells.push('<td class="'+(key===todayKey?'jh-today':'')+'"><input class="jh-dot jh-off" type="checkbox" disabled><span class="jh-stamp"></span></td>');
        continue;
      }

      ruleTotal++; total++;
      const task=RV_habitOccurrence(rule,key);
      const done=!!(task&&task.status==="Done");
      if(done){ruleDone++;doneTotal++;}

      const stamp=done
        ? (typeof TB_fmtStamp==="function"
            ? TB_fmtStamp(task.doneAt||task.statusUpdatedAt)
            : String(task.doneAt||task.statusUpdatedAt||""))
        : "";

      const rid=String(rule.id||"");
      cells.push(
        '<td class="'+(key===todayKey?'jh-today':'')+'">'+
          '<input class="jh-dot" type="checkbox" '+(done?'checked':'')+
          ' data-rid="'+esc(rid)+'" data-date="'+esc(key)+'" '+
          'title="'+esc(done?("Done: "+stamp):"Mark done")+'" '+
          'onchange="RV_habitSetDone(this.dataset.rid,this.dataset.date,this.checked)">'+
          '<span class="jh-stamp">'+(done?esc(stamp):'')+'</span>'+
        '</td>'
      );
    }

    return '<tr>'+
      '<td class="jh-name"><div class="jh-habit-title">'+esc(rule.title||"Recurring task")+'</div>'+
      '<div class="jh-habit-meta">'+esc(rule.kind||"Recurring")+(rule.start?' · '+esc(rule.start):'')+'</div></td>'+
      cells.join("")+
      '<td class="jh-progress">'+ruleDone+'/'+ruleTotal+'</td>'+
    '</tr>';
  }).join("");

  host.innerHTML=
    '<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin:4px 0 8px">'+
      '<b>MONTH: <i>'+esc(monthName)+'</i> '+x.year+'</b>'+
      '<span class="jh-progress">'+doneTotal+' / '+total+' completed</span>'+
    '</div>'+
    '<div class="jh-wrap"><table class="jh-table">'+
      '<thead><tr><th class="jh-name">DAILY HABIT</th>'+headDays+'<th>DONE</th></tr></thead>'+
      '<tbody>'+body+'</tbody>'+
    '</table></div>';

  if(summary)summary.textContent=doneTotal+" / "+total+" completed";
}
function RV_renderSummary(data){
  const totalIncome=data.reduce((s,x)=>s+(x.money.totalIn||0),0);
  const totalExpense=data.reduce((s,x)=>s+(x.money.totalOut||0),0);
  const totalSaving=data.reduce((s,x)=>s+x.money.saving,0);
  const xym=RV_selectedYM();
  const monthEnd=new Date(xym.year,xym.month+1,0);
  const overallRemaining=typeof moneyCumulativeBalanceAt==="function"?moneyCumulativeBalanceAt(monthEnd):0;
  const totalDone=data.reduce((s,x)=>s+x.tasks.done,0);
  const remainingMap={};
  data.forEach(function(day){
    (day.tasks.rows||[]).forEach(function(t){
      if(t.planDate!==day.key)return;
      if(String(t.status||"Not Started")!=="Done"){
        remainingMap[t.id||("rv-"+day.key+"-"+String(t.title||""))]=t;
      }
    });
  });
  const totalPending=Object.keys(remainingMap).length;

  const sleepDays=data.filter(x=>x.health.sleepMinutes>0);
  const sleepAvg=sleepDays.length?sleepDays.reduce((s,x)=>s+x.health.sleepMinutes,0)/sleepDays.length:0;
  const calDays=data.filter(x=>x.health.calories>0);
  const calAvg=calDays.length?calDays.reduce((s,x)=>s+x.health.calories,0)/calDays.length:0;
  const latestWeight=[...data].reverse().find(x=>x.health.weight!=null);

  const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};
  set("rvIncome",RV_rupee(totalIncome));
  set("rvExpense",RV_rupee(totalExpense));
  set("rvSaving",RV_rupee(overallRemaining));
  set("rvSleep",sleepAvg?HL_fmtMinutes(Math.round(sleepAvg)):"0h");
  set("rvTasksDone",totalDone);
  set("rvTasksPending",totalPending);
  set("rvCalories",calAvg?Math.round(calAvg).toLocaleString("en-IN"):"0");
  set("rvWeight",latestWeight?latestWeight.health.weight.toFixed(1)+" kg":"—");
}
function RV_renderCalendar(data){
  const grid=document.getElementById("rvCalendarGrid");
  if(!grid)return;

  const x=RV_selectedYM();
  const title=document.getElementById("rvCalendarTitle");
  if(title){
    title.textContent=RV_monthNames()[x.month]+" "+x.year+" — "+RV_metricLabel(RV_selectedMetric||"all");
  }

  const first=new Date(x.year,x.month,1);
  const offset=(first.getDay()+6)%7;
  const today=RV_key(new Date());
  let html="";

  for(let i=0;i<offset;i++){
    html+='<div class="rv-day rv-day-empty"></div>';
  }

  (data||[]).forEach(function(d,idx){
    const metric=RV_selectedMetric||"all";
    const has=RV_hasMetric(d,metric);
    let lines="";

    if(metric==="all"){
      lines=
        '<span class="rv-money-income">💵 Income '+RV_rupee(d.money.totalIn||0)+'</span>'+
        '<span class="rv-money-expense">💸 Expenses '+RV_rupee(d.money.totalOut||0)+'</span>'+
        '<span class="rv-money-saving">🏦 Savings '+RV_rupee(d.money.saving||0)+'</span>'+
        '<span class="rv-money-remaining">💰 Remaining '+RV_rupee(d.money.overallRemaining||0)+'</span>'+
        (d.health.sleepMinutes?'<span>😴 Sleep '+HL_fmtMinutes(d.health.sleepMinutes)+'</span>':'')+
        (d.tasks.done?'<span class="good">✅ Done '+d.tasks.done+'</span>':'')+
        (d.tasks.notStarted?'<span class="pending">📌 Not Started '+d.tasks.notStarted+'</span>':'')+
        (d.health.calories?'<span>🍽️ '+Math.round(d.health.calories)+' kcal</span>':'')+
        (d.health.weight!=null?'<span>⚖️ '+Number(d.health.weight).toFixed(1)+' kg</span>':'');
    }else{
      lines=RV_metricLine(d,metric);
    }

    html+='<div class="rv-day '+(d.key===today?"today ":"")+(has?"":"metric-missing")+'" onclick="RV_openDay(\''+d.key+'\')">'+
      '<div class="rv-day-num"><span>'+(idx+1)+'</span>'+(!has?'<small>Missing</small>':'')+'</div>'+
      '<div class="rv-day-lines">'+lines+
      (!has?'<div class="rv-metric-missing-note">'+RV_metricMissingText(metric)+' — click to enter</div>':'')+
      '</div></div>';
  });

  grid.innerHTML=html;
}
function RV_renderTrend(data){
  const b=document.getElementById("rvTrendBars");if(!b)return;
  const max=Math.max(1,...data.map(x=>Math.max(x.money.income,x.money.expense,x.money.saving)));
  b.innerHTML=data.map(function(x,i){
    const ih=x.money.income?Math.max(3,Math.round((x.money.income/max)*145)):1;
    const eh=x.money.expense?Math.max(3,Math.round((x.money.expense/max)*145)):1;
    const sh=x.money.saving?Math.max(3,Math.round((x.money.saving/max)*145)):1;
    return '<div class="rv-trend-day"><div class="rv-trend-stack">'+
      '<i title="Income '+RV_rupee(x.money.income)+'" style="height:'+ih+'px;background:#22c55e"></i>'+
      '<i title="Expense '+RV_rupee(x.money.expense)+'" style="height:'+eh+'px;background:#ef4444"></i>'+
      '<i title="Savings '+RV_rupee(x.money.saving)+'" style="height:'+sh+'px;background:#3b82f6"></i>'+
      '</div><small>'+(i+1)+'</small></div>';
  }).join("");
}
function RV_renderAll(){
  if(typeof RV_selectedMetric==="undefined" || !RV_selectedMetric){
    RV_selectedMetric="all";
  }

  try{RV_initSelectors();}catch(err){console.error("Review selectors:",err);}

  let data=[];
  try{
    data=RV_monthData();
  }catch(err){
    console.error("Review month data failed:",err);

    // Calendar must still render even when one data source fails.
    const x=RV_selectedYM();
    const last=new Date(x.year,x.month+1,0).getDate();
    for(let d=1;d<=last;d++){
      const key=RV_key(new Date(x.year,x.month,d));
      data.push({
        key:key,
        money:{income:0,expense:0,saving:0,totalIn:0,totalOut:0,netMovement:0,overallRemaining:0,txCount:0},
        health:{calories:0,sleepMinutes:0,weight:null},
        tasks:{rows:[],done:0,notStarted:0,inProgress:0,hold:0,total:0}
      });
    }
  }

  try{RV_renderHabitTracker();}catch(err){console.error("Journal habit tracker failed:",err);}
  try{RV_renderSummary(data);}catch(err){console.error("Review summary failed:",err);}
  try{RV_renderCalendar(data);}catch(err){console.error("Review calendar failed:",err);}
  try{RV_renderTrend(data);}catch(err){console.error("Review trend failed:",err);}
}

/* -------- Auto-sync Google Sheet before Review renders -------- */
async function RV_syncMoneySheet(showMessage){
  if(RV_sheetSyncInProgress)return [];
  RV_sheetSyncInProgress=true;

  const s=document.getElementById("rvSyncStatus");
  const btn=document.querySelector(".rv-sync-btn");
  if(s){
    s.textContent="Syncing complete website sheet…";
    s.className="rv-sync-status";
  }
  if(btn)btn.disabled=true;

  try{
    const rows=await syncFromGoogleSheet(false);

    let diag={};
    try{diag=JSON.parse(localStorage.getItem("lastGoogleSyncDiagnostics")||"{}")}catch(e){}

    if(s){
      s.textContent="✓ "+rows.length+" transactions"+
        (diag.sheetLastRow?(" · last row "+diag.sheetLastRow):"")+
        (diag.firstDate&&diag.lastDate?(" · "+diag.firstDate+" → "+diag.lastDate):"");
      s.className="rv-sync-status ok";
    }

    RV_renderAll();

    if(showMessage){
      alert(
        "Review synced with the full website sheet.\n\n"+
        "Transactions: "+rows.length+
        (diag.sheetLastRow?("\nSheet last row: "+diag.sheetLastRow):"")+
        (diag.firstDate?("\nFirst date: "+diag.firstDate):"")+
        (diag.lastDate?("\nLast date: "+diag.lastDate):"")
      );
    }
    return rows;
  }catch(err){
    console.error("Review Sheet sync failed:",err);
    if(s){
      s.textContent="Sync failed — "+err.message;
      s.className="rv-sync-status bad";
    }
    RV_renderAll();
    if(showMessage){
      alert("Review sync failed.\n"+err.message);
    }
    return [];
  }finally{
    RV_sheetSyncInProgress=false;
    if(btn)btn.disabled=false;
  }
}
async function RV_openReview(){
  RV_initSelectors();

  // Draw Review immediately from current local data.
  RV_renderAll();

  // Then refresh Sheet data without blocking the page.
  if(!RV_reviewInitialized){
    RV_reviewInitialized=true;
    setTimeout(function(){
      RV_syncMoneySheet(false);
    },50);
  }
}

/* -------- Remaining tasks popup -------- */
function RV_openRemainingTasksPopup(){
  const x=RV_selectedYM();
  const monthPrefix=String(x.year)+"-"+String(x.month+1).padStart(2,"0")+"-";
  let rows=[];

  try{
    rows=(typeof TB_loadTasks==="function"?TB_loadTasks():[]).filter(function(t){
      return String(t.planDate||"").startsWith(monthPrefix) &&
             String(t.status||"Not Started")!=="Done";
    });
  }catch(e){
    console.error("Remaining task popup failed:",e);
  }

  rows.sort(function(a,b){
    const da=String(a.planDate||"");
    const db=String(b.planDate||"");
    if(da!==db)return da.localeCompare(db);
    return String(a.startTime||"").localeCompare(String(b.startTime||""));
  });

  const existing=document.getElementById("rvRemainingTasksModal");
  if(existing)existing.remove();

  const modal=document.createElement("div");
  modal.id="rvRemainingTasksModal";
  modal.className="tools-modal";
  modal.style.display="flex";
  modal.onclick=function(e){if(e.target===modal)modal.remove();};

  const monthName=(typeof RV_monthNames==="function"?RV_monthNames()[x.month]:"Selected month");
  const counts={
    notStarted:rows.filter(function(t){return String(t.status||"Not Started")==="Not Started";}).length,
    inProgress:rows.filter(function(t){return String(t.status||"")==="In Progress";}).length,
    hold:rows.filter(function(t){return String(t.status||"")==="Hold";}).length
  };

  const body=rows.length
    ? '<div style="overflow:auto;max-height:62vh"><table class="category-transaction-table" style="min-width:760px">'+
      '<thead><tr><th>Date</th><th>Task</th><th>Type</th><th>Time</th><th>Minutes</th><th>Status</th></tr></thead><tbody>'+
      rows.map(function(t){
        const safeId=String(t.id||"").replace(/\\/g,"\\\\").replace(/'/g,"\\'");
        return '<tr>'+
          '<td>'+esc(typeof TB_fmtDate==="function"?TB_fmtDate(t.planDate):String(t.planDate||""))+'</td>'+
          '<td><b>'+esc(t.title||"Task")+'</b></td>'+
          '<td>'+esc(t.type||"")+'</td>'+
          '<td>'+esc(t.startTime||"—")+'</td>'+
          '<td>'+esc(String(Number(t.estimate)||20))+'</td>'+
          '<td><select onchange="RV_changeTaskStatus(\''+safeId+'\',this.value);RV_openRemainingTasksPopup()">'+
            ["Not Started","In Progress","Hold","Done"].map(function(s){
              return '<option '+(String(t.status||"Not Started")===s?"selected":"")+'>'+s+'</option>';
            }).join("")+
          '</select></td>'+
        '</tr>';
      }).join("")+
      '</tbody></table></div>'
    : '<div class="card" style="text-align:center"><h3>🎉 No remaining tasks</h3><p class="muted">Everything planned for this month is done.</p></div>';

  modal.innerHTML=
    '<div class="modal-box" style="width:min(1000px,96vw)">'+
      '<div class="modal-head">'+
        '<div><h2 style="margin:0">📌 Remaining Tasks — '+esc(monthName+" "+x.year)+'</h2>'+
        '<p class="muted" style="margin:5px 0 0">'+rows.length+' remaining · '+counts.notStarted+' Not Started · '+counts.inProgress+' In Progress · '+counts.hold+' Hold</p></div>'+
        '<button onclick="document.getElementById(\'rvRemainingTasksModal\').remove()">✕</button>'+
      '</div>'+
      '<div style="margin-top:16px">'+body+'</div>'+
    '</div>';

  document.body.appendChild(modal);
}

/* -------- Day drilldown -------- */
function RV_openDay(key){
  RV_selectedDate=key;
  const d=RV_dayData(key),modal=document.getElementById("rvDayModal");
  if(!modal)return;

  document.getElementById("rvDayTitle").textContent="🗓️ "+(typeof TB_fmtDate==="function"?TB_fmtDate(key):key);
  document.getElementById("rvDaySubtitle").textContent="Review and correct this date";

  const m=d.money,h=d.health,t=d.tasks;
  let taskHtml='<div class="rv-day-task-list"><h3>📌 Tasks</h3>';
  if(!t.rows.length)taskHtml+='<div class="muted">No tasks recorded for this date.</div>';
  else taskHtml+=t.rows.map(function(row){
    return '<div class="rv-day-task-row"><b>'+esc(row.title||"Task")+'</b><span>'+esc(row.type||"")+'</span>'+
      '<select onchange="RV_changeTaskStatus(\''+row.id+'\',this.value)">'+
      ["Not Started","In Progress","Done","Hold"].map(s=>'<option '+(row.status===s?"selected":"")+'>'+s+'</option>').join("")+
      '</select></div>';
  }).join("");
  taskHtml+='</div>';

  document.getElementById("rvDayBody").innerHTML=
    '<div class="rv-day-summary">'+
      '<div><span>⬇️ Total In</span><b>'+RV_rupee(m.totalIn)+'</b></div>'+
      '<div><span>⬆️ Total Out</span><b>'+RV_rupee(m.totalOut)+'</b></div>'+
      '<div><span>💰 Overall Remaining</span><b>'+RV_rupee(m.overallRemaining)+'</b></div>'+
      '<div><span>😴 Sleep</span><b>'+(h.sleepMinutes?HL_fmtMinutes(h.sleepMinutes):"—")+'</b></div>'+
      '<div><span>✅ Tasks Done</span><b>'+t.done+'</b></div>'+
      '<div><span>📌 Not Started</span><b>'+t.notStarted+'</b></div>'+
      '<div><span>🍽️ Calories</span><b>'+(h.calories?Math.round(h.calories)+" kcal":"—")+'</b></div>'+
      '<div><span>⚖️ Weight</span><b>'+(h.weight!=null?h.weight.toFixed(1)+" kg":"—")+'</b></div>'+
    '</div>'+taskHtml;

  RV_prepareQuickEntry();
  RV_autoOpenEntryForMetric();
  modal.style.display="flex";
}
function RV_closeDay(){const m=document.getElementById("rvDayModal");if(m)m.style.display="none";}
function RV_changeTaskStatus(id,status){
  try{
    const tasks=TB_loadTasks(),t=tasks.find(x=>x.id===id);if(!t)return;
    t.status=status;
    if(typeof TB_setStatusTimestamp==="function")TB_setStatusTimestamp(t,status);
    TB_saveTasks(tasks);
    if(typeof TB_renderStatusDashboard==="function")TB_renderStatusDashboard();
    RV_renderAll();RV_openDay(RV_selectedDate);
  }catch(e){console.error(e)}
}

function RV_showEntryTab(name,btn){
  document.querySelectorAll(".rv-entry-panel").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".rv-entry-tabs button").forEach(x=>x.classList.remove("active"));
  const p=document.getElementById("rvEntry"+name.charAt(0).toUpperCase()+name.slice(1));
  if(p)p.classList.add("active");
  if(btn)btn.classList.add("active");
}
function RV_autoOpenEntryForMetric(){
  const map={
    income:["money","Income"],
    expense:["money","Needs"],
    saving:["money","Savings"],
    sleep:["sleep",null],
    calories:["calories",null],
    weight:["weight",null],
    done:["tasks",null],
    pending:["tasks",null]
  };
  const x=map[RV_selectedMetric];
  if(!x)return;
  const tab=[...document.querySelectorAll(".rv-entry-tabs button")].find(b=>b.textContent.toLowerCase().includes(x[0]==="money"?"money":x[0]));
  RV_showEntryTab(x[0],tab);
  if(x[1]){
    const main=document.getElementById("rvMoneyMain");
    if(main && [...main.options].some(o=>o.value===x[1])){main.value=x[1];RV_updateMoneySubs();}
  }
}
function RV_prepareQuickEntry(){
  const main=document.getElementById("rvMoneyMain"),account=document.getElementById("rvMoneyAccount");
  if(main){
    const groups=(typeof config!=="undefined"&&config.categories)?Object.keys(config.categories):["Needs","Wants","Income","Savings"];
    main.innerHTML=groups.map(g=>'<option value="'+esc(g)+'">'+esc(g)+'</option>').join("");
    const preferred=groups.find(g=>g.toLowerCase()==="needs")||groups[0];
    if(preferred)main.value=preferred;
  }
  if(account){
    const accounts=(typeof config!=="undefined"&&Array.isArray(config.accounts))?config.accounts:[];
    account.innerHTML=accounts.length?accounts.map(a=>'<option value="'+esc(a)+'">'+esc(a)+'</option>').join(""):'<option value="">Account</option>';
  }
  RV_updateMoneySubs();
  const s=RV_healthForDate(RV_selectedDate);
  const w=document.getElementById("rvWeightValue");if(w)w.value=s.weight!=null?s.weight:"";
}
function RV_updateMoneySubs(){
  const main=document.getElementById("rvMoneyMain"),sub=document.getElementById("rvMoneySub");if(!main||!sub)return;
  const arr=(typeof config!=="undefined"&&config.categories&&config.categories[main.value])?config.categories[main.value]:[];
  sub.innerHTML=arr.length?arr.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join(""):'<option value="Other">Other</option>';
}
async function RV_saveMoneyQuick(){
  const amount=Number((document.getElementById("rvMoneyAmount")||{}).value||0);
  const main=(document.getElementById("rvMoneyMain")||{}).value||"Needs";
  const sub=(document.getElementById("rvMoneySub")||{}).value||"Other";
  const account=(document.getElementById("rvMoneyAccount")||{}).value||"";
  const explanation=(document.getElementById("rvMoneyExplanation")||{}).value||"Review quick entry";
  if(!RV_selectedDate||!amount){alert("Enter an amount.");return}

  const entry={date:RV_selectedDate,mainCategory:main,subCategory:sub,explanation:explanation,amount:amount,account:account,fromAccount:account,toAccount:""};
  try{
    if(typeof addTransactionToGoogleSheet!=="function")throw new Error("Google Sheet save is unavailable.");
    await addTransactionToGoogleSheet(entry);
    await RV_syncMoneySheet(false);
  }catch(err){
    await syncFromGoogleSheet(false).catch(function(){});
    alert("Transaction NOT saved to Google Sheet. Nothing was added to the website.\n"+((err&&err.message)||err));
    return;
  }
  if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
  RV_renderAll();RV_openDay(RV_selectedDate);
}
function RV_saveCaloriesQuick(){
  const meal=(document.getElementById("rvCalMeal")||{}).value||"Snacks";
  const food=(document.getElementById("rvCalFood")||{}).value||"Quick calorie entry";
  const cal=Math.max(0,Number((document.getElementById("rvCalValue")||{}).value)||0);
  if(!RV_selectedDate||!cal){alert("Enter calories.");return}
  const arr=typeof HL_foods==="function"?HL_foods():JSON.parse(localStorage.getItem("healthFoodsV1")||"[]");
  arr.push({id:"rvfood-"+Date.now(),date:RV_selectedDate,meal:meal,food:food,qty:1,unit:"entry",calories:cal,manual:true});
  localStorage.setItem("healthFoodsV1",JSON.stringify(arr));
  if(typeof HL_renderAll==="function")HL_renderAll();
  RV_renderAll();RV_openDay(RV_selectedDate);
}
function RV_saveWeightQuick(){
  const v=Number((document.getElementById("rvWeightValue")||{}).value||0);
  if(!RV_selectedDate||!v){alert("Enter weight.");return}
  let arr=typeof HL_weights==="function"?HL_weights():JSON.parse(localStorage.getItem("healthWeightsV1")||"[]");
  arr=arr.filter(x=>x.date!==RV_selectedDate);arr.push({date:RV_selectedDate,weight:v});arr.sort((a,b)=>a.date.localeCompare(b.date));
  localStorage.setItem("healthWeightsV1",JSON.stringify(arr));
  if(typeof HL_renderAll==="function")HL_renderAll();
  RV_renderAll();RV_openDay(RV_selectedDate);
}
function RV_saveSleepQuick(){
  const s=(document.getElementById("rvSleepStart")||{}).value,e=(document.getElementById("rvSleepEnd")||{}).value;
  if(!RV_selectedDate||!s||!e){alert("Enter sleep and wake time.");return}
  const minutes=typeof HL_minutesBetween==="function"?HL_minutesBetween(s,e):0;
  let arr=typeof HL_sleeps==="function"?HL_sleeps():JSON.parse(localStorage.getItem("healthSleepV1")||"[]");
  arr=arr.filter(x=>x.date!==RV_selectedDate);arr.push({date:RV_selectedDate,start:s,end:e,minutes:minutes});arr.sort((a,b)=>a.date.localeCompare(b.date));
  localStorage.setItem("healthSleepV1",JSON.stringify(arr));
  if(typeof HL_renderAll==="function")HL_renderAll();
  RV_renderAll();RV_openDay(RV_selectedDate);
}
function RV_saveTaskQuick(){
  const title=(document.getElementById("rvTaskTitle")||{}).value.trim();
  const mins=Math.max(1,Number((document.getElementById("rvTaskMinutes")||{}).value)||20);
  const status=(document.getElementById("rvTaskStatus")||{}).value||"Not Started";
  if(!RV_selectedDate||!title){alert("Enter a task name.");return}
  const tasks=TB_loadTasks(),now=new Date().toISOString();
  const t={id:"rvtask-"+Date.now(),priority:"",title:title,type:"Personal",estimate:mins,startTime:"",manualTime:false,autoTime:true,planDate:RV_selectedDate,status:status,completedDate:"",actualMinutes:0,source:"review",createdAt:now,startedAt:"",holdAt:"",doneAt:"",statusUpdatedAt:now};
  if(typeof TB_setStatusTimestamp==="function")TB_setStatusTimestamp(t,status);
  tasks.push(t);TB_saveTasks(tasks);
  if(typeof TB_recalculateAutoTimes==="function")TB_recalculateAutoTimes(RV_selectedDate);
  if(typeof TB_renderStatusDashboard==="function")TB_renderStatusDashboard();
  RV_renderAll();RV_openDay(RV_selectedDate);
}
</script>

<div id="clearMoneyModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:9999;align-items:center;justify-content:center;padding:20px">
  <div style="background:white;width:min(520px,95vw);border-radius:16px;padding:24px;box-shadow:0 20px 60px rgba(0,0,0,.25)">
    <h2 style="margin-top:0;color:#b42318">🗑️ Clear All Money Data?</h2>
    <p>This will clear <b>every Money-section data item</b> stored by this tracker:</p>
    <ul style="line-height:1.7">
      <li>Uploaded sheet transactions</li>
      <li>Manual money entries</li>
      <li>Income, Expenses, Savings and Loan totals</li>
      <li>Imported transaction table</li>
      <li>Money category/account customizations</li>
    </ul>
    <p style="color:#b42318;font-weight:700">This cannot be undone.</p>
    <div id="clearError" style="display:none;color:#b42318;margin:10px 0"></div>
    <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:18px">
      <button class="secondary" onclick="closeClearMoneyModal()">Cancel</button>
      <button style="background:#dc2626;color:white;padding:10px 16px;border-radius:8px;font-weight:700" onclick="confirmClearAllMoneyData()">Yes, Clear Everything</button>
    </div>
  </div>
</div>
<div id="clearDone" style="display:none;position:fixed;right:24px;bottom:24px;z-index:10000;background:#065f46;color:white;padding:12px 16px;border-radius:10px;box-shadow:0 8px 25px rgba(0,0,0,.2)">✓ All Money data cleared</div>

<script>
/* ============================================================
   V117 — GENERAL NOTES + DASHBOARD HUB
   ============================================================ */
let NT_notes=[];

function MT_openPage(id){
  const btn=[...document.querySelectorAll(".nav")].find(function(b){
    return (b.getAttribute("onclick")||"").indexOf("'"+id+"'")!==-1;
  });
  showPage(id,btn||null);
}

function NT_today(){
  const d=new Date();
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
}
function NT_setStatus(msg,ok){
  const el=document.getElementById("ntStatusMsg");
  if(!el)return;
  el.textContent=msg;
  el.style.color=ok===true?"#15803d":ok===false?"#dc2626":"#64748b";
}
function NT_clearEditor(){
  ["ntId","ntTitle","ntCategory","ntBody"].forEach(function(id){
    const e=document.getElementById(id); if(e)e.value="";
  });
  const d=document.getElementById("ntDate"); if(d)d.value=NT_today();
  const s=document.getElementById("ntStatus"); if(s)s.value="Active";
  const h=document.getElementById("ntEditorTitle"); if(h)h.textContent="✍️ New Note";
  NT_setStatus("Ready",null);
}
function NT_loadNotes(showMessage){
  const list=document.getElementById("ntNotesList");
  if(list)list.innerHTML='<div class="muted">Loading notes from Google Sheet...</div>';
  NT_setStatus("Syncing...",null);

  if(!(window.google && google.script && google.script.run)){
    NT_setStatus("Google Apps Script connection is not available.",false);
    return;
  }

  google.script.run
    .withSuccessHandler(function(result){
      if(!result || !result.success){
        NT_setStatus((result&&result.message)||"Could not load Notes sheet.",false);
        return;
      }
      NT_notes=Array.isArray(result.notes)?result.notes:[];
      NT_refreshFilters();
      NT_renderNotes();
      NT_setStatus("Synced ✓",true);
      if(showMessage) alert("Notes synced from Google Sheet.");
    })
    .withFailureHandler(function(err){
      NT_setStatus((err&&err.message)||String(err),false);
    })
    .NT_getNotesForWeb();
}
function NT_refreshFilters(){
  const sel=document.getElementById("ntFilter");
  if(!sel)return;
  const current=sel.value||"ALL";
  const cats=[...new Set(NT_notes.map(function(n){return String(n.category||"").trim()}).filter(Boolean))].sort();
  sel.innerHTML='<option value="ALL">All Categories</option>'+cats.map(function(c){
    return '<option value="'+esc(c)+'">'+esc(c)+'</option>';
  }).join("");
  if(cats.indexOf(current)!==-1)sel.value=current;
}
function NT_renderNotes(){
  const box=document.getElementById("ntNotesList");
  if(!box)return;
  const q=String((document.getElementById("ntSearch")||{}).value||"").trim().toLowerCase();
  const filter=String((document.getElementById("ntFilter")||{}).value||"ALL");

  let rows=NT_notes.slice().filter(function(n){
    if(filter!=="ALL" && String(n.category||"")!==filter)return false;
    if(!q)return true;
    return [n.title,n.category,n.body,n.status,n.date].join(" ").toLowerCase().indexOf(q)!==-1;
  });

  rows.sort(function(a,b){
    return String(b.updatedAt||b.date||"").localeCompare(String(a.updatedAt||a.date||""));
  });

  const count=document.getElementById("ntCount");
  if(count)count.textContent=rows.length+" note"+(rows.length===1?"":"s");

  if(!rows.length){
    box.innerHTML='<div class="muted">No notes found.</div>';
    return;
  }

  box.innerHTML=rows.map(function(n){
    return '<div class="mt-note-card">'+
      '<div class="mt-note-card-head"><div>'+
        '<h3>'+esc(n.title||"Untitled")+'</h3>'+
        '<div class="mt-note-meta">'+esc(n.date||"")+' · '+esc(n.updatedAt||"")+'</div>'+
      '</div><div><span class="mt-note-tag">'+esc(n.status||"Active")+'</span></div></div>'+
      '<div style="margin-top:8px"><span class="mt-note-tag">'+esc(n.category||"General")+'</span></div>'+
      '<div class="mt-note-body">'+esc(n.body||"")+'</div>'+
      '<div class="mt-note-card-actions">'+
        '<button class="secondary" onclick="NT_editNote(\''+String(n.id||"").replace(/'/g,"\\'")+'\')">✏️ Edit</button>'+
        '<button class="remove" onclick="NT_deleteNote(\''+String(n.id||"").replace(/'/g,"\\'")+'\')">🗑 Delete</button>'+
      '</div>'+
    '</div>';
  }).join("");
}
function NT_editNote(id){
  const n=NT_notes.find(function(x){return String(x.id)===String(id)});
  if(!n)return;
  document.getElementById("ntId").value=n.id||"";
  document.getElementById("ntDate").value=n.date||NT_today();
  document.getElementById("ntTitle").value=n.title||"";
  document.getElementById("ntCategory").value=n.category||"";
  document.getElementById("ntStatus").value=n.status||"Active";
  document.getElementById("ntBody").value=n.body||"";
  document.getElementById("ntEditorTitle").textContent="✏️ Edit Note";
  window.scrollTo({top:0,behavior:"smooth"});
}
function NT_saveNote(){
  const payload={
    id:document.getElementById("ntId").value.trim(),
    date:document.getElementById("ntDate").value||NT_today(),
    title:document.getElementById("ntTitle").value.trim(),
    category:document.getElementById("ntCategory").value.trim()||"General",
    status:document.getElementById("ntStatus").value||"Active",
    body:document.getElementById("ntBody").value.trim()
  };
  if(!payload.title && !payload.body){
    alert("Enter a title or note.");
    return;
  }
  const btn=document.getElementById("ntSaveBtn");
  if(btn){btn.disabled=true;btn.textContent="Saving...";}
  NT_setStatus("Saving to Google Sheet...",null);

  google.script.run
    .withSuccessHandler(function(result){
      if(btn){btn.disabled=false;btn.textContent="💾 Save Note";}
      if(!result || !result.success){
        NT_setStatus((result&&result.message)||"Save failed.",false);
        return;
      }
      NT_clearEditor();
      NT_setStatus("Saved ✓",true);
      NT_loadNotes(false);
    })
    .withFailureHandler(function(err){
      if(btn){btn.disabled=false;btn.textContent="💾 Save Note";}
      NT_setStatus((err&&err.message)||String(err),false);
    })
    .NT_saveNoteForWeb(payload);
}
function NT_deleteNote(id){
  if(!confirm("Delete this note from the website and Google Sheet?"))return;
  NT_setStatus("Deleting...",null);
  google.script.run
    .withSuccessHandler(function(result){
      if(!result || !result.success){
        NT_setStatus((result&&result.message)||"Delete failed.",false);
        return;
      }
      NT_clearEditor();
      NT_loadNotes(false);
    })
    .withFailureHandler(function(err){
      NT_setStatus((err&&err.message)||String(err),false);
    })
    .NT_deleteNoteForWeb(id);
}

// Extend the existing page opener without replacing it.
(function(){
  const oldShowPage=window.showPage;
  window.showPage=function(id,btn){
    oldShowPage(id,btn);
    if(id==="notes"){
      const d=document.getElementById("ntDate");
      if(d && !d.value)d.value=NT_today();
      NT_loadNotes(false);
    }
  };
})();

// ======================================================
// V156 STRICT STARTUP MASTER
// Never display a transaction left from an older browser cache.
// On page load, clear transaction cache and read Google Sheet ONCE.
// No timer / no periodic refresh.
// ======================================================
try{
  localStorage.removeItem("moneyEntries");
  localStorage.removeItem("lastGoogleSyncDiagnostics");
}catch(_e){}

let MW_initialSheetLoaded=false;
async function MW_initialGoogleSheetLoad(){
  if(MW_initialSheetLoaded)return;
  MW_initialSheetLoaded=true;
  try{
    await syncFromGoogleSheet(false);
    if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
    if(typeof RV_renderAll==="function")RV_renderAll();
    // Do not force Bank Wise re-render here; prevents wiping a form being typed.
  }catch(err){
    console.warn("Initial Google Sheet load failed:",err);
    // Cache stays empty: no Sheet data = no website transactions.
    try{localStorage.setItem("moneyEntries","[]");}catch(_e){}
  }
}
window.addEventListener("load",function(){
  MW_initialGoogleSheetLoad();
});

// ======================================================
// V156 MANUAL REFRESH ONLY
// No timer, no focus refresh, no automatic page refresh.
// This prevents the form from disappearing while typing.
// Website -> Sheet happens ONLY when Save & Sync is clicked.
// Sheet -> Website happens ONLY when the user refreshes/syncs.
// ======================================================
async function MW_manualMasterSync(){
  // Immediately remove every browser transaction before contacting Google Sheet.
  localStorage.setItem("moneyEntries","[]");
  if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
  if(typeof RV_renderAll==="function")RV_renderAll();
  if(document.getElementById("bankWiseArea") && typeof renderBankWiseView==="function")renderBankWiseView();

  // Now rebuild transaction data ONLY from Google Sheet.
  const rows=await syncFromGoogleSheet(false);

  if(typeof updateMoneyDashboard==="function")updateMoneyDashboard();
  if(typeof RV_renderAll==="function")RV_renderAll();
  if(document.getElementById("bankWiseArea") && typeof renderBankWiseView==="function")renderBankWiseView();
  return rows;
}


/* ===== Separate Habit Tracker ===== */
const HB_KEY="myTracking_habits_v2",HB_LOG_KEY="myTracking_habit_logs_v2";
function HB_load(){try{return JSON.parse(localStorage.getItem(HB_KEY)||"[]")}catch(e){return []}}
function HB_store(a){localStorage.setItem(HB_KEY,JSON.stringify(a))}
function HB_logs(){try{return JSON.parse(localStorage.getItem(HB_LOG_KEY)||"{}")}catch(e){return {}}}
function HB_storeLogs(a){localStorage.setItem(HB_LOG_KEY,JSON.stringify(a))}
function HB_key(y,m,d){return y+"-"+String(m).padStart(2,"0")+"-"+String(d).padStart(2,"0")}
function HB_frequencyChanged(){const f=document.getElementById("hbFrequency").value;document.getElementById("hbWeekWrap").style.display=f==="Weekly"?"block":"none";document.getElementById("hbMonthDayWrap").style.display=f==="Monthly"?"block":"none"}
function HB_openEditor(id){
 const h=HB_load().find(x=>x.id===id);document.getElementById("hbId").value=h?h.id:"";document.getElementById("hbName").value=h?h.name:"";document.getElementById("hbFrequency").value=h?h.frequency:"Daily";document.getElementById("hbTime").value=h?h.time:"";document.getElementById("hbMonthDay").value=h?h.monthDay||1:1;
 document.querySelectorAll(".hbDow").forEach(c=>c.checked=!!(h&&(h.days||[]).map(Number).includes(Number(c.value))));document.getElementById("hbEditorTitle").textContent=h?"Edit Habit":"Add Habit";HB_frequencyChanged();document.getElementById("hbEditor").style.display="flex";
}
function HB_closeEditor(){document.getElementById("hbEditor").style.display="none"}
function HB_saveHabit(){
 const name=document.getElementById("hbName").value.trim();if(!name){alert("Enter habit name.");return}
 const frequency=document.getElementById("hbFrequency").value,days=[...document.querySelectorAll(".hbDow:checked")].map(c=>Number(c.value));if(frequency==="Weekly"&&!days.length){alert("Select at least one weekday.");return}
 const id=document.getElementById("hbId").value||("hb-"+Date.now()),all=HB_load(),i=all.findIndex(x=>x.id===id),h={id,name,frequency,time:document.getElementById("hbTime").value,days,monthDay:Number(document.getElementById("hbMonthDay").value)||1};
 if(i>=0)all[i]=h;else all.push(h);HB_store(all);HB_closeEditor();HB_renderAll();
}
function HB_delete(id){const h=HB_load().find(x=>x.id===id);if(!h||!confirm('Delete habit "'+h.name+'"?'))return;HB_store(HB_load().filter(x=>x.id!==id));const l=HB_logs();Object.keys(l).forEach(k=>{if(k.startsWith(id+"|"))delete l[k]});HB_storeLogs(l);HB_renderAll()}
function HB_match(h,y,m,d){const dt=new Date(y,m-1,d);if(h.frequency==="Daily")return true;if(h.frequency==="Weekly")return (h.days||[]).map(Number).includes(dt.getDay());return Number(h.monthDay||1)===d}
function HB_toggle(id,date,checked){const l=HB_logs(),k=id+"|"+date;if(checked)l[k]={done:true,at:new Date().toISOString()};else delete l[k];HB_storeLogs(l);HB_renderAll()}

function HB_allHabits(){
  const out=[];
  const seen={};

  // Existing recurring tasks from Time: these recreate the previous habit tracker.
  if(typeof TB_loadRecurring==="function"){
    TB_loadRecurring().filter(function(r){return r&&r.active!==false;}).forEach(function(r){
      const h={
        id:String(r.id),
        name:r.title||"Recurring task",
        frequency:r.kind||"Daily",
        time:r.start||"",
        source:"time",
        original:r
      };
      seen[h.id]=true;
      out.push(h);
    });
  }

  // Habits created directly from the Habits tab.
  HB_load().forEach(function(h){
    if(!h||!h.id||seen[h.id])return;
    out.push(Object.assign({},h,{source:"habit"}));
  });
  return out;
}
function HB_isActive(h,y,m,d){
  if(h.source==="time" && h.original && typeof TB_recurringMatchesDate==="function"){
    return TB_recurringMatchesDate(h.original,HB_key(y,m,d));
  }
  return HB_match(h,y,m,d);
}
function HB_doneInfo(h,key){
  if(h.source==="time"){
    const task=typeof RV_habitOccurrence==="function"?RV_habitOccurrence(h.original,key):null;
    return task&&task.status==="Done"
      ? {done:true,at:task.doneAt||task.statusUpdatedAt||""}
      : {done:false,at:""};
  }
  const log=HB_logs()[h.id+"|"+key];
  return log&&log.done?{done:true,at:log.at||""}:{done:false,at:""};
}
function HB_toggleUnified(id,date,checked,source){
  if(source==="time"){
    if(typeof RV_habitSetDone==="function")RV_habitSetDone(id,date,checked);
    setTimeout(HB_renderAll,0);
    return;
  }
  HB_toggle(id,date,checked);
}
function HB_editUnified(id,source){
  if(source==="time"){
    alert("This habit comes from Time → Recurring Tasks. Edit it there so Time and Habits stay synchronized.");
    return;
  }
  HB_openEditor(id);
}
function HB_deleteUnified(id,source){
  if(source==="time"){
    const r=typeof TB_loadRecurring==="function"?TB_loadRecurring().find(function(x){return String(x.id)===String(id)}):null;
    if(!r)return;
    if(!confirm('Delete recurring task "'+(r.title||"")+'" from Time and Habits?'))return;
    if(typeof TB_saveRecurring==="function"){
      TB_saveRecurring(TB_loadRecurring().filter(function(x){return String(x.id)!==String(id)}));
      if(typeof TB_syncVisibleRecurringDates==="function")TB_syncVisibleRecurringDates();
    }
    HB_renderAll();
    return;
  }
  HB_delete(id);
}

function HB_renderAll(){
  const host=document.getElementById("hbGrid");
  if(!host)return;

  const month=document.getElementById("hbMonth");
  if(!month.value){
    const n=new Date();
    month.value=n.getFullYear()+"-"+String(n.getMonth()+1).padStart(2,"0");
  }

  const p=month.value.split("-");
  const y=Number(p[0]),m=Number(p[1]);
  const days=new Date(y,m,0).getDate();
  const habits=HB_allHabits();
  const now=new Date();
  const today=HB_key(now.getFullYear(),now.getMonth()+1,now.getDate());
  let total=0,done=0;

  if(!habits.length){
    host.innerHTML='<div style="text-align:center;padding:28px"><h3>No habits yet</h3><p class="muted">Add a habit here or create a recurring task in Time.</p><button class="primary" onclick="HB_openEditor()">＋ Add Habit</button></div>';
    document.getElementById("hbSummary").textContent="0 habits";
    return;
  }

  const heads=Array.from({length:days},function(_,i){
    const key=HB_key(y,m,i+1);
    return '<th class="'+(key===today?'hb-today':'')+'">'+(i+1)+'</th>';
  }).join("");

  const rows=habits.map(function(h){
    let ht=0,hd=0,cells="";
    for(let d=1;d<=days;d++){
      const key=HB_key(y,m,d);
      const active=HB_isActive(h,y,m,d);
      const info=active?HB_doneInfo(h,key):{done:false,at:""};
      if(active){ht++;total++;if(info.done){hd++;done++;}}
      const stamp=info.done&&info.at?new Date(info.at).toLocaleString("en-IN"):"";
      cells+='<td class="'+(key===today?'hb-today':'')+'">'+
        '<input class="hb-dot '+(!active?'hb-off':'')+'" type="checkbox" '+(info.done?'checked':'')+' '+(!active?'disabled':'')+
        ' data-id="'+esc(h.id)+'" data-date="'+key+'" data-source="'+h.source+'" title="'+esc(stamp||"Mark done")+'" '+
        'onchange="HB_toggleUnified(this.dataset.id,this.dataset.date,this.checked,this.dataset.source)">'+
        '</td>';
    }

    return '<tr><td>'+
      '<div class="hb-name">'+esc(h.name)+'</div>'+
      '<div class="hb-meta">'+esc(h.frequency)+(h.time?' · '+esc(h.time):'')+(h.source==="time"?' · Time recurring':'')+'</div>'+
      '<div class="hb-actions">'+
        '<button data-id="'+esc(h.id)+'" data-source="'+h.source+'" onclick="HB_editUnified(this.dataset.id,this.dataset.source)">✏️ Edit</button>'+
        '<button data-id="'+esc(h.id)+'" data-source="'+h.source+'" onclick="HB_deleteUnified(this.dataset.id,this.dataset.source)">🗑 Delete</button>'+
      '</div></td>'+
      cells+'<td><b>'+hd+'/'+ht+'</b></td></tr>';
  }).join("");

  host.innerHTML='<div style="margin-bottom:10px"><b>MONTH: '+new Date(y,m-1,1).toLocaleDateString("en-IN",{month:"long"})+' '+y+'</b></div>'+
    '<div class="hb-wrap"><table class="hb-table"><thead><tr><th>DAILY HABIT</th>'+heads+'<th>DONE</th></tr></thead><tbody>'+rows+'</tbody></table></div>';

  document.getElementById("hbSummary").textContent=done+" / "+total+" completed";
}
function HB_openCircular(){
  const month=document.getElementById("hbMonth");
  if(!month.value)HB_renderAll();

  const p=month.value.split("-");
  const y=Number(p[0]),m=Number(p[1]);
  const days=new Date(y,m,0).getDate();
  const habits=HB_allHabits();

  if(!habits.length){
    document.getElementById("hbCircularBody").innerHTML="<p>No habits yet.</p>";
    document.getElementById("hbCircularModal").style.display="flex";
    return;
  }

  const c=320,base=90;
  const ring=Math.min(27,Math.max(14,190/Math.max(1,habits.length)));
  let svg='<svg viewBox="0 0 640 640" style="width:min(640px,100%);display:block;margin:auto">';

  habits.forEach(function(h,i){
    for(let d=1;d<=days;d++){
      if(!HB_isActive(h,y,m,d))continue;
      const key=HB_key(y,m,d);
      const info=HB_doneInfo(h,key);
      const a=(d-1)/days*Math.PI*2-Math.PI/2;
      const r=base+i*ring;
      const x=c+Math.cos(a)*r,yy=c+Math.sin(a)*r;
      svg+='<circle cx="'+x.toFixed(1)+'" cy="'+yy.toFixed(1)+'" r="7" fill="'+(info.done?'#22c55e':'#fff')+'" stroke="#94a3b8" stroke-width="2">'+
        '<title>'+esc(h.name)+' · Day '+d+(info.done?' · Done':'')+'</title></circle>';
    }
  });

  const rr=base+habits.length*ring+24;
  for(let d=1;d<=days;d++){
    const a=(d-1)/days*Math.PI*2-Math.PI/2;
    const x=c+Math.cos(a)*rr,yy=c+Math.sin(a)*rr;
    svg+='<text x="'+x.toFixed(1)+'" y="'+yy.toFixed(1)+'" text-anchor="middle" dominant-baseline="middle" font-size="10">'+d+'</text>';
  }
  svg+='</svg>';

  document.getElementById("hbCircularBody").innerHTML=
    svg+'<div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">'+
    habits.map(function(h){return '<span><b>'+esc(h.name)+'</b></span>';}).join("")+'</div>';
  document.getElementById("hbCircularModal").style.display="flex";
}
function HB_closeCircular(){document.getElementById("hbCircularModal").style.display="none"}

/* ==================== SCHEDULE ==================== */
const SC_KEY="myTracking_schedule_v1";
let SC_view="daily";
function SC_load(){try{return JSON.parse(localStorage.getItem(SC_KEY)||"[]")}catch(e){return []}}
function SC_store(a){localStorage.setItem(SC_KEY,JSON.stringify(a))}
function SC_iso(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function SC_parse(k){const p=String(k).split("-").map(Number);return new Date(p[0],p[1]-1,p[2])}
const SC_WAKE_KEY="myTracking_schedule_wake_v1";
function SC_wakes(){try{return JSON.parse(localStorage.getItem(SC_WAKE_KEY)||"{}")}catch(e){return {}}}
function SC_saveWake(){const date=document.getElementById("scDate").value;if(!date)return;const a=SC_wakes(),v=document.getElementById("scWake").value;if(v)a[date]=v;else delete a[date];localStorage.setItem(SC_WAKE_KEY,JSON.stringify(a))}
function SC_getWake(date){return SC_wakes()[date]||"05:00"}
function SC_minutes(t){if(!t)return null;const p=t.split(":").map(Number);return p[0]*60+p[1]}
function SC_timeFromMinutes(n){n=Math.max(0,Math.min(1439,n));return String(Math.floor(n/60)).padStart(2,"0")+":"+String(n%60).padStart(2,"0")}
function SC_actualHTML(x){if(!x.actualStart&&!x.actualEnd&&!x.actualTitle)return "";const time=(x.actualStart||"—")+(x.actualEnd?" – "+x.actualEnd:"");return '<div class="sc-actual-event" data-id="'+esc(x.id)+'" onclick="event.stopPropagation();SC_openEditor(this.dataset.id)"><b>'+esc(x.actualTitle||x.title)+'</b><small>'+esc(time)+' · Actual</small></div>'}
function SC_init(){const e=document.getElementById("scDate");if(e&&!e.value)e.value=SC_iso(new Date())}
function SC_today(){document.getElementById("scDate").value=SC_iso(new Date());SC_render()}
function SC_setView(v){
 SC_view=v;
 ["daily","weekly","monthly"].forEach(x=>{
   document.getElementById("sc"+x[0].toUpperCase()+x.slice(1)+"View").style.display=x===v?"block":"none";
   document.getElementById("sc"+x[0].toUpperCase()+x.slice(1)+"Btn").classList.toggle("primary",x===v);
 });
 SC_render();
}
function SC_openEditor(id,date,start){
 const item=SC_load().find(x=>x.id===id);
 SC_init();
 document.getElementById("scId").value=item?item.id:"";
 document.getElementById("scEditDate").value=item?item.date:(date||document.getElementById("scDate").value);
 document.getElementById("scTitle").value=item?item.title:"";
 document.getElementById("scStart").value=item?item.start:(start||"08:00");
 document.getElementById("scEnd").value=item?item.end:"";
 document.getElementById("scType").value=item?item.type:"Personal";
 document.getElementById("scActualStart").value=item?(item.actualStart||""):"";
 document.getElementById("scActualEnd").value=item?(item.actualEnd||""):"";
 document.getElementById("scActualTitle").value=item?(item.actualTitle||""):"";
 document.getElementById("scNotes").value=item?item.notes:"";
 document.getElementById("scEditorTitle").textContent=item?"Edit Schedule":"Add Schedule";
 document.getElementById("scDeleteBtn").style.display=item?"inline-block":"none";
 document.getElementById("scEditor").style.display="flex";
}
function SC_closeEditor(){document.getElementById("scEditor").style.display="none"}
function SC_save(){
 const title=document.getElementById("scTitle").value.trim(),date=document.getElementById("scEditDate").value,start=document.getElementById("scStart").value;
 if(!title||!date||!start){alert("Enter date, title and start time.");return}
 const id=document.getElementById("scId").value||("sc-"+Date.now()+"-"+Math.random().toString(16).slice(2));
 const a=SC_load(),i=a.findIndex(x=>x.id===id);
 const item={id,date,title,start,end:document.getElementById("scEnd").value,type:document.getElementById("scType").value,actualStart:document.getElementById("scActualStart").value,actualEnd:document.getElementById("scActualEnd").value,actualTitle:document.getElementById("scActualTitle").value.trim(),notes:document.getElementById("scNotes").value.trim()};
 if(i>=0)a[i]=item;else a.push(item);
 SC_store(a);SC_closeEditor();document.getElementById("scDate").value=date;SC_render();
}
function SC_deleteCurrent(){
 const id=document.getElementById("scId").value;if(!id)return;
 if(!confirm("Delete this schedule item?"))return;
 SC_store(SC_load().filter(x=>x.id!==id));SC_closeEditor();SC_render();
}
function SC_items(date){return SC_load().filter(x=>x.date===date).sort((a,b)=>String(a.start).localeCompare(String(b.start)))}
function SC_eventHTML(x,mini){
 const time=x.start+(x.end?" – "+x.end:"");
 return '<div class="'+(mini?"sc-mini-event":"sc-event")+'" data-id="'+esc(x.id)+'" onclick="event.stopPropagation();SC_openEditor(this.dataset.id)"><b>'+esc(x.title)+'</b><small>'+esc(time)+(x.type?" · "+esc(x.type):"")+'</small></div>';
}
function SC_directValue(date,time,kind){
 const a=SC_items(date);
 if(kind==="plan"){const x=a.find(v=>v.start===time);return x?x.title:"";}
 const x=a.find(v=>v.actualStart===time);return x?(x.actualTitle||x.title):"";
}
function SC_directSave(date,time,kind,value,el){
 value=String(value||"").trim();let a=SC_load();
 if(kind==="plan"){
   let i=a.findIndex(x=>x.date===date&&x.start===time);
   if(!value){if(i>=0){if(a[i].actualStart||a[i].actualTitle)a[i].title="";else a.splice(i,1);}}
   else if(i>=0)a[i].title=value;
   else a.push({id:"sc-"+Date.now()+"-"+Math.random().toString(16).slice(2),date,title:value,start:time,end:"",type:"Personal",actualStart:"",actualEnd:"",actualTitle:"",notes:""});
 }else{
   let i=a.findIndex(x=>x.date===date&&x.actualStart===time);
   if(i<0)i=a.findIndex(x=>x.date===date&&x.start===time);
   if(!value){if(i>=0){a[i].actualStart="";a[i].actualEnd="";a[i].actualTitle="";}}
   else if(i>=0){a[i].actualStart=time;a[i].actualTitle=value;}
   else a.push({id:"sc-"+Date.now()+"-"+Math.random().toString(16).slice(2),date,title:"",start:time,end:"",type:"Personal",actualStart:time,actualEnd:"",actualTitle:value,notes:""});
 }
 SC_store(a);
 if(el){const s=el.parentElement.querySelector(".sc-direct-saved");if(s){s.classList.add("show");setTimeout(()=>s.classList.remove("show"),700);}}
}
function SC_directInput(date,time,kind,value){
 return '<div class="sc-direct-cell"><input class="sc-direct-input" value="'+esc(value||"")+'" placeholder="'+(kind==="plan"?"Type what you plan...":"Type what actually happened...")+'" data-date="'+date+'" data-time="'+time+'" data-kind="'+kind+'" onblur="SC_directSave(this.dataset.date,this.dataset.time,this.dataset.kind,this.value,this)" onkeydown="if(event.key===&quot;Enter&quot;){event.preventDefault();this.blur()}"><span class="sc-direct-saved">Saved</span></div>';
}
function SC_renderDaily(){
 const key=document.getElementById("scDate").value,d=SC_parse(key),host=document.getElementById("scDailyView"),wake=SC_getWake(key);
 document.getElementById("scWake").value=wake;const start=SC_minutes(wake),end=23*60+30;let rows="";
 for(let min=start;min<=end;min+=30){
  const t=SC_timeFromMinutes(min),next=SC_timeFromMinutes(Math.min(min+30,1439));
  rows+='<div class="sc-time">'+t+' – '+next+'</div><div class="sc-slot sc-direct-plan">'+SC_directInput(key,t,"plan",SC_directValue(key,t,"plan"))+'</div><div class="sc-slot sc-actual sc-direct-actual">'+SC_directInput(key,t,"actual",SC_directValue(key,t,"actual"))+'</div>';
 }
 host.innerHTML='<div class="sc-day-head"><div><h2 style="margin:0">'+d.toLocaleDateString("en-IN",{weekday:"long",day:"numeric",month:"long",year:"numeric"})+'</h2><span class="muted">Simply type directly in Planned or Actual. Press Enter or click outside to save.</span></div><button class="primary" onclick="SC_openEditor()">＋ Detailed Entry</button></div><div class="sc-wake-banner">⏰ Wake-up time: '+wake+' · Schedule begins from this exact time.</div><div class="sc-dual-wrap"><div class="sc-dual-head"><div>Time</div><div>📝 What I Planned</div><div>✅ What Actually Happened</div></div><div class="sc-dual">'+rows+'</div></div>';
}
function SC_weekStart(d){const x=new Date(d),day=x.getDay(),diff=day===0?-6:1-day;x.setDate(x.getDate()+diff);return x}
function SC_renderWeekly(){
 const selected=SC_parse(document.getElementById("scDate").value),start=SC_weekStart(selected),days=Array.from({length:7},(_,i)=>{const d=new Date(start);d.setDate(start.getDate()+i);return d});
 let head='<th></th>'+days.map(d=>'<th>'+d.toLocaleDateString("en-IN",{weekday:"short"})+'<br>'+d.getDate()+' '+d.toLocaleDateString("en-IN",{month:"short"})+'</th>').join("");
 let plan='<tr><td class="sc-week-time"><b>📝 Planned</b></td>',actual='<tr><td class="sc-week-time"><b>✅ Actual</b></td>';
 days.forEach(d=>{const key=SC_iso(d),items=SC_items(key);plan+='<td data-date="'+key+'" onclick="SC_openEditor(null,this.dataset.date)">'+items.map(x=>SC_eventHTML(x,true)).join("")+'</td>';actual+='<td>'+items.map(x=>SC_actualHTML(x)).join("")+'</td>'});
 plan+='</tr>';actual+='</tr>';
 document.getElementById("scWeeklyView").innerHTML='<div class="sc-day-head"><h2 style="margin:0">Weekly Plan vs Actual</h2><span class="muted">See what you planned and what really happened</span></div><div class="sc-week"><table class="sc-week-table"><thead><tr>'+head+'</tr></thead><tbody>'+plan+actual+'</tbody></table></div>';
}
function SC_renderMonthly(){
 const selected=SC_parse(document.getElementById("scDate").value),y=selected.getFullYear(),m=selected.getMonth(),first=new Date(y,m,1),offset=(first.getDay()+6)%7,start=new Date(y,m,1-offset);let cells="";
 for(let i=0;i<42;i++){const d=new Date(start);d.setDate(start.getDate()+i);const key=SC_iso(d),same=d.getMonth()===m,items=SC_items(key);
 const planned=items.slice(0,3).map(x=>'<div class="sc-month-event" data-id="'+esc(x.id)+'" onclick="event.stopPropagation();SC_openEditor(this.dataset.id)">📝 '+esc(x.start+' '+x.title)+'</div>').join("");
 const actual=items.filter(x=>x.actualStart||x.actualTitle).slice(0,3).map(x=>'<div class="sc-month-event" style="background:#dcfce7" data-id="'+esc(x.id)+'" onclick="event.stopPropagation();SC_openEditor(this.dataset.id)">✅ '+esc((x.actualStart||"")+' '+(x.actualTitle||x.title))+'</div>').join("");
 cells+='<div class="sc-month-cell '+(!same?'sc-muted':'')+'" data-date="'+key+'" onclick="SC_openEditor(null,this.dataset.date)"><div class="sc-month-num">'+d.getDate()+'</div>'+planned+actual+'</div>'}
 document.getElementById("scMonthlyView").innerHTML='<div class="sc-day-head"><h2 style="margin:0">'+selected.toLocaleDateString("en-IN",{month:"long",year:"numeric"})+' — Plan vs Actual</h2><span class="muted">📝 Planned · ✅ Actual</span></div><div class="sc-month-grid">'+cells+'</div>';
}
function SC_render(){SC_init();const k=document.getElementById("scDate").value;document.getElementById("scWake").value=SC_getWake(k);SC_renderDaily();SC_renderWeekly();SC_renderMonthly()}
</script>

<datalist id="roomSharingPeopleList"></datalist>
</body>
</html>

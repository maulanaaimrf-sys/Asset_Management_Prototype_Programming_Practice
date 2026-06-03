from tabulate import tabulate
from datetime import datetime
import pwinput

APP_NAME    = "AssetHub Investment Tracker"
APP_SLOGAN  = "Monitor & Manage your Investment Portfolio Efficiently"
PIN_AKSES   = "1234"
LEBAR       = 70  

## Database Portfolio

portfolio = [
    {
        'asset_id'      : 'AST001',
        'asset_name'    : 'Bitcoin',
        'category'      : 'Crypto',
        'quantity'      : 0.5000,
        'buy_price'     : 900000000,
        'market_price'  : 980000000,
        'status'        : 'Active',
        'purchase_date' : '2024-01-15'
    },
    {
        'asset_id'      : 'AST002',
        'asset_name'    : 'Gold',
        'category'      : 'Commodity',
        'quantity'      : 10.0000,
        'buy_price'     : 1850000,
        'market_price'  : 1925000,
        'status'        : 'Active',
        'purchase_date' : '2024-02-20'
    },
    {
        'asset_id'      : 'AST003',
        'asset_name'    : 'BBCA',
        'category'      : 'Indonesia Stock',
        'quantity'      : 100.0000,
        'buy_price'     : 9500,
        'market_price'  : 10300,
        'status'        : 'Active',
        'purchase_date' : '2024-03-10'
    },
    {
        'asset_id'      : 'AST004',
        'asset_name'    : 'NVIDIA',
        'category'      : 'US Stock',
        'quantity'      : 15.0000,
        'buy_price'     : 1450000,
        'market_price'  : 1680000,
        'status'        : 'Active',
        'purchase_date' : '2024-04-05'
    }
]

## Transaction History ##
transaction_history = []

# Asset Category
ASSET_CATEGORIES = ['Crypto','Commodity','Indonesia Stock','US Stock','Real Estate','Mutual Fund','Cash','Others']

# Helper Functions

def format_rupiah(value):
    return f"Rp {value:,.0f}"

def print_header(title):
    print(f"\n{'═' * LEBAR}")
    print(title.upper().center(LEBAR))
    print(f"{'═' * LEBAR}")

def print_divider(char='─'):
    print(char * LEBAR)

def print_success(pesan):
    print(f"\n  ✔  {pesan}")

def print_error(pesan):
    print(f"\n  ✘  {pesan}")

def print_info(pesan):
    print(f"\n  ℹ  {pesan}")

def input_angka(prompt, tipe='float'):
    while True:
        try:
            nilai = input(f"  {prompt}")
            if tipe == 'float':
                return float(nilai)
            elif tipe == 'int':
                return int(nilai)
        except ValueError:
            print_error("Please enter a valid number.")

def input_kategori():
    while True:
        print()
        data = [[i + 1, kat] for i, kat in enumerate(ASSET_CATEGORIES)]
        print(tabulate(
            data,
            headers=["#", "Category"],
            tablefmt="simple_outline",
            colalign=("center", "left")
        ))

        pilihan = input("\n  Select number or type category name : ").strip()

        if pilihan.isdigit():
            idx = int(pilihan) - 1
            if 0 <= idx < len(ASSET_CATEGORIES):
                return ASSET_CATEGORIES[idx]

        elif pilihan.title() in ASSET_CATEGORIES:
            return pilihan.title()

        print_error("Invalid category. Please select from the list.")

def cari_asset(asset_id):
    for i in range(len(portfolio)):
        if portfolio[i]['asset_id'].upper() == asset_id.upper():
            return i
    return -1

def validasi_asset_id(asset_id):
    asset_id = asset_id.upper()

    if not (asset_id.startswith('AST') and asset_id[3:].isdigit() and len(asset_id) > 3):
        print_error("Asset ID format must be 'AST' followed by numbers (e.g. AST005).")
        return False

    if cari_asset(asset_id) != -1:
        print_error(f"Asset ID '{asset_id}' already exists in portfolio.")
        return False

    return True

def back_menu():
    print()
    while True:
        back = input("  Press [0] to return to main menu : ")
        if back == '0':
            break
        else:
            print_error("Invalid input. Press 0 to return.")

def konfirmasi_aksi(prompt="Confirm action? (Y/N) : "):
    return input(f"\n  {prompt}").strip().upper() == 'Y'

def print_summary_box(rows, title="SUMMARY", width=45):
    # Lebar kolom kiri & kanan dihitung otomatis dari konten
    col_kiri  = max(len(label) for label, _ in rows)
    col_kanan = max(len(nilai) for _, nilai in rows)
    inner     = col_kiri + col_kanan + 3      # 3 = spasi " : "
    width     = max(width, inner + 4)         # +4 untuk padding kiri-kanan

    garis_atas   = f"┌{'─' * (width)}┐"
    garis_header = f"├{'─' * (width)}┤"
    garis_bawah  = f"└{'─' * (width)}┘"

    print(garis_atas)
    print(f"│{title.upper().center(width)}│")
    print(garis_header)

    for label, nilai in rows:
        baris = f"  {label:<{col_kiri}}  :  {nilai:>{col_kanan}}  "
        print(f"│{baris:{width}}│")

    print(garis_bawah)


# LOGIN System

def login():
    kesempatan = 3

    while kesempatan > 0:
        print(f'''
{"─" * LEBAR}

{APP_NAME.center(LEBAR)}
{APP_SLOGAN.center(LEBAR)}

{"─" * LEBAR}
''')

        pin = pwinput.pwinput("  Enter Access PIN : ", mask="*")

        if pin == PIN_AKSES:
            print(f'''
{"═" * LEBAR}
{"✔  LOGIN SUCCESSFUL".center(LEBAR)}
{"═" * LEBAR}
''')
            return True

        kesempatan -= 1

        if kesempatan > 0:
            print(f'''
{"═" * LEBAR}
{"✘  INVALID PIN".center(LEBAR)}
{f"Remaining Attempts : {kesempatan}".center(LEBAR)}
{"═" * LEBAR}
''')
        else:
            print(f'''
{"═" * LEBAR}
{"ACCESS DENIED".center(LEBAR)}
{"Maximum login attempts exceeded.".center(LEBAR)}
{"Program will now terminate.".center(LEBAR)}
{"═" * LEBAR}
''')

    return False

# View Portfolio

def tampilkan_portfolio():

    if len(portfolio) == 0:
        print_info("Your portfolio is currently empty.")
        return

    data = []
    total_investasi    = 0
    total_profit       = 0
    total_market_value = 0

    for i in range(len(portfolio)):
        market_value  = portfolio[i]['quantity'] * portfolio[i]['market_price']
        investasi     = portfolio[i]['quantity'] * portfolio[i]['buy_price']
        unrealized_pl = market_value - investasi

        total_investasi    += investasi
        total_profit       += unrealized_pl
        total_market_value += market_value

        pl_label = f"+{format_rupiah(unrealized_pl)}" if unrealized_pl >= 0 else format_rupiah(unrealized_pl)

        row = [
            i + 1,
            portfolio[i]['asset_id'],
            portfolio[i]['asset_name'],
            portfolio[i]['category'],
            f"{portfolio[i]['quantity']:.4f}",
            format_rupiah(portfolio[i]['buy_price']),
            format_rupiah(portfolio[i]['market_price']),
            format_rupiah(market_value),
            pl_label,
            portfolio[i]['status']
        ]

        data.append(row)

    tabel = tabulate(
        data,
        headers=["No", "Asset ID", "Asset Name", "Category", "Quantity", "Avg Cost", "Market Price", "Market Value", "Unrealized P/L", "Status"],
        tablefmt="fancy_grid"
    )

    lebar_tabel = len(tabel.splitlines()[0])

    print(f"\n{'═' * lebar_tabel}")
    print("PORTFOLIO OVERVIEW".center(lebar_tabel))
    print(f"{'═' * lebar_tabel}")
    print(tabel)

    if total_investasi > 0:
        persen_profit = (total_profit / total_investasi) * 100
    else:
        persen_profit = 0

    pl_total_label = f"+{format_rupiah(total_profit)}" if total_profit >= 0 else format_rupiah(total_profit)
    roi_label      = f"+{persen_profit:.2f}%" if persen_profit >= 0 else f"{persen_profit:.2f}%"

    print()
    print_summary_box([
        ("Total Investment",     format_rupiah(total_investasi)),
        ("Portfolio Value",      format_rupiah(total_market_value)),
        ("Unrealized P/L",       pl_total_label),
        ("Return on Investment", roi_label),
    ], title="PORTFOLIO SUMMARY")


# ADD Asset

def tambah_asset():

    print_header("Add New Asset")

    while True:
        asset_id = input("\n  Enter Asset ID (e.g. AST005) : ").strip()
        if validasi_asset_id(asset_id):
            asset_id = asset_id.upper()
            break

    asset_name = input("  Enter Asset Name            : ").strip().title()

    if not asset_name:
        print_error("Asset name cannot be empty.")
        return

    print("\n  Select Asset Category :")
    category = input_kategori()

    quantity = input_angka("Enter Quantity              : ", 'float')
    if quantity <= 0:
        print_error("Quantity must be greater than 0.")
        return

    buy_price = input_angka("Enter Average Cost (Rp)     : ", 'float')
    if buy_price <= 0:
        print_error("Average Cost must be greater than 0.")
        return

    market_price = input_angka("Enter Current Price (Rp)    : ", 'float')
    if market_price <= 0:
        print_error("Current Price must be greater than 0.")
        return

    total_investasi    = quantity * buy_price
    total_market_value = quantity * market_price
    profit_loss        = total_market_value - total_investasi
    pl_label           = f"+{format_rupiah(profit_loss)}" if profit_loss >= 0 else format_rupiah(profit_loss)

    print()
    print(tabulate(
        [
            ["Asset ID",         asset_id],
            ["Asset Name",       asset_name],
            ["Category",         category],
            ["Quantity",         f"{quantity:.4f}"],
            ["Average Cost",     format_rupiah(buy_price)],
            ["Current Price",    format_rupiah(market_price)],
            ["Total Investment", format_rupiah(total_investasi)],
            ["Market Value",     format_rupiah(total_market_value)],
            ["Unrealized P/L",   pl_label],
        ],
        headers=["  ASSET PREVIEW", ""],
        tablefmt="simple_outline",
        colalign=("left", "right")
    ))

    if not konfirmasi_aksi("Confirm add this asset? (Y/N) : "):
        print_info("Asset addition cancelled.")
        return

    portfolio.append({
        'asset_id'      : asset_id,
        'asset_name'    : asset_name,
        'category'      : category,
        'quantity'      : quantity,
        'buy_price'     : buy_price,
        'market_price'  : market_price,
        'status'        : 'Active',
        'purchase_date' : datetime.now().strftime('%Y-%m-%d')
    })

    print_success(f"Asset '{asset_name}' ({asset_id}) successfully added to portfolio.")


# Update Asset

def update_asset():

    print_header("Update Asset")
    tampilkan_portfolio()

    asset_id = input("\n  Enter Asset ID to update : ").upper()
    idx = cari_asset(asset_id)
    if idx == -1:
        print_error(f"Asset ID '{asset_id}' not found in portfolio.")
        return

    asset_name = portfolio[idx]['asset_name']

    print()
    print(tabulate(
        [
            ["1", "Update Quantity"],
            ["2", "Update Average Cost"],
            ["3", "Update Current Price"],
            ["4", "Update Status"],
            ["5", "Update Multiple Fields"],
            ["0", "Cancel"],
        ],
        headers=["#", f"  UPDATE MENU  ─  {asset_id} ({asset_name})"],
        tablefmt="simple_outline",
        colalign=("center", "left")
    ))

    pilihan = input("\n  Select option : ")
    if pilihan == '0':
        print_info("Update cancelled.")
        return

    elif pilihan == '1':
        qty_baru = input_angka("Enter New Quantity : ", 'float')
        if qty_baru <= 0:
            print_error("Quantity must be greater than 0.")
            return
        if not konfirmasi_aksi("Confirm update Quantity? (Y/N) : "):
            print_info("Update cancelled.")
            return
        portfolio[idx]['quantity'] = qty_baru
        print_success("Quantity updated successfully.")

    elif pilihan == '2':
        buy_price_baru = input_angka("Enter New Average Cost (Rp) : ", 'float')
        if buy_price_baru <= 0:
            print_error("Average Cost must be greater than 0.")
            return
        if not konfirmasi_aksi("Confirm update Average Cost? (Y/N) : "):
            print_info("Update cancelled.")
            return
        portfolio[idx]['buy_price'] = buy_price_baru
        print_success("Average Cost updated successfully.")

    elif pilihan == '3':
        market_price_baru = input_angka("Enter New Current Price (Rp) : ", 'float')
        if market_price_baru <= 0:
            print_error("Current Price must be greater than 0.")
            return
        if not konfirmasi_aksi("Confirm update Current Price? (Y/N) : "):
            print_info("Update cancelled.")
            return
        portfolio[idx]['market_price'] = market_price_baru
        print_success("Current Price updated successfully.")

    elif pilihan == '4':
        print_info("Available status : Active / Inactive")
        status_baru = input("  Enter New Status : ").strip().title()
        if status_baru not in ['Active', 'Inactive']:
            print_error("Invalid status. Enter 'Active' or 'Inactive'.")
            return
        if not konfirmasi_aksi("Confirm update Status? (Y/N) : "):
            print_info("Update cancelled.")
            return
        portfolio[idx]['status'] = status_baru
        print_success(f"Status updated to '{status_baru}'.")

    elif pilihan == '5':
     
        qty_baru          = portfolio[idx]['quantity']
        buy_price_baru    = portfolio[idx]['buy_price']
        market_price_baru = portfolio[idx]['market_price']
        ada_error         = False

        print_info("Type a new value or press Enter to skip each field.")

        qty_input = input("  New Quantity (or skip) : ").strip()
        if qty_input.lower() not in ('skip', ''):
            try:
                nilai = float(qty_input)
                if nilai <= 0:
                    raise ValueError()
                qty_baru = nilai
            except:
                print_error("Invalid quantity — update cancelled.")
                ada_error = True

        buy_input = input("  New Average Cost (or skip) : ").strip()
        if buy_input.lower() not in ('skip', '') and not ada_error:
            try:
                nilai = float(buy_input)
                if nilai <= 0:
                    raise ValueError()
                buy_price_baru = nilai
            except:
                print_error("Invalid Average Cost — update cancelled.")
                ada_error = True

        market_input = input("  New Current Price (or skip) : ").strip()

        if market_input.lower() not in ('skip', '') and not ada_error:
            try:
                nilai = float(market_input)
                if nilai <= 0:
                    raise ValueError()
                market_price_baru = nilai
            except:
                print_error("Invalid Current Price — update cancelled.")
                ada_error = True

        if ada_error:
            return

        if not konfirmasi_aksi("Confirm update all changes? (Y/N) : "):
            print_info("Update cancelled.")
            return

        portfolio[idx]['quantity']     = qty_baru
        portfolio[idx]['buy_price']    = buy_price_baru
        portfolio[idx]['market_price'] = market_price_baru

        print_success(f"Asset '{asset_name}' successfully updated.")

    else:
        print_error("Invalid option. Please select 0–5.")


# Delete Asset

def delete_asset():

    print_header("Delete Asset")
    tampilkan_portfolio()

    asset_id = input("\n  Enter Asset ID to delete : ").upper()
    idx = cari_asset(asset_id)
    if idx == -1:
        print_error(f"Asset ID '{asset_id}' not found in portfolio.")
        return

    asset_name = portfolio[idx]['asset_name']

    print_info(f"You are about to permanently delete '{asset_name}' ({asset_id}).")

    if konfirmasi_aksi(f"Confirm delete '{asset_name}'? (Y/N) : "):
        del portfolio[idx]
        print_success(f"Asset '{asset_name}' ({asset_id}) has been deleted.")
    else:
        print_info("Deletion cancelled.")


# BUY / SELL Transaction

def transaksi_asset():

    print_header("Buy / Sell Transaction")
    tampilkan_portfolio()

    asset_id = input("\n  Enter Asset ID : ").upper()
    idx = cari_asset(asset_id)
    if idx == -1:
        print_error(f"Asset ID '{asset_id}' not found in portfolio.")
        return

    asset_name = portfolio[idx]['asset_name']

    print()
    print(tabulate(
        [
            ["1", "BUY  — Add to position"],
            ["2", "SELL — Reduce position"],
        ],
        headers=["#", f"  TRANSACTION  ─  {asset_id} ({asset_name})"],
        tablefmt="simple_outline",
        colalign=("center", "left")
    ))

    transaksi = input("\n  Select transaction type : ")
    if transaksi not in ('1', '2'):
        print_error("Invalid selection. Enter 1 (BUY) or 2 (SELL).")
        return

    qty   = input_angka("Enter Quantity          : ", 'float')
    harga = input_angka("Enter Price per Unit    : ", 'float')
    if qty <= 0 or harga <= 0:
        print_error("Quantity and price must be greater than 0.")
        return

    total_transaksi = qty * harga
    if transaksi == '1':
        
        qty_lama       = portfolio[idx]['quantity']
        buy_price_lama = portfolio[idx]['buy_price']
        qty_baru       = qty_lama + qty
        avg_price_baru = ((qty_lama * buy_price_lama) + (qty * harga)) / qty_baru

        portfolio[idx]['quantity']     = qty_baru
        portfolio[idx]['buy_price']    = avg_price_baru
        portfolio[idx]['market_price'] = harga

        transaction_history.append({
            'asset_id'         : asset_id,
            'asset_name'       : asset_name,
            'transaction_type' : 'BUY',
            'quantity'         : qty,
            'price'            : harga,
            'total'            : total_transaksi,
            'date'             : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        print_success(f"BUY order executed — {qty:.4f} {asset_name} @ {format_rupiah(harga)}")
        print(f"     Total           : {format_rupiah(total_transaksi)}")
        print(f"     New Avg Cost    : {format_rupiah(avg_price_baru)}")
        print(f"     Total Position  : {qty_baru:.4f} units")

    elif transaksi == '2':

        if qty > portfolio[idx]['quantity']:
            print_error(f"Insufficient quantity. Available : {portfolio[idx]['quantity']:.4f} units.")
            return

        portfolio[idx]['quantity']     -= qty
        portfolio[idx]['market_price']  = harga     

        transaction_history.append({
            'asset_id'         : asset_id,
            'asset_name'       : asset_name,
            'transaction_type' : 'SELL',
            'quantity'         : qty,
            'price'            : harga,
            'total'            : total_transaksi,
            'date'             : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        sisa = portfolio[idx]['quantity']

        print_success(f"SELL order executed — {qty:.4f} {asset_name} @ {format_rupiah(harga)}")
        print(f"     Total Proceeds  : {format_rupiah(total_transaksi)}")
        print(f"     Remaining Qty   : {sisa:.4f} units")


# Transaction History

def tampilkan_transaksi():
    print_header("Transaction History")

    if len(transaction_history) == 0:
        print_info("No transactions recorded yet.")
        return

    data = []

    for i in range(len(transaction_history)):
        tipe  = transaction_history[i]['transaction_type']
        label = f"▲ {tipe}" if tipe == 'BUY' else f"▼ {tipe}"

        row = [
            i + 1,
            transaction_history[i]['asset_id'],
            transaction_history[i]['asset_name'],
            label,
            f"{transaction_history[i]['quantity']:.4f}",
            format_rupiah(transaction_history[i]['price']),
            format_rupiah(transaction_history[i]['total']),
            transaction_history[i]['date']
        ]

        data.append(row)

    print(tabulate(
        data,
        headers=["No", "Asset ID", "Asset Name", "Type", "Qty", "Price/Unit", "Total Value", "Date & Time"],
        tablefmt="fancy_grid"
    ))

    total_beli  = sum(t['total'] for t in transaction_history if t['transaction_type'] == 'BUY')
    total_jual  = sum(t['total'] for t in transaction_history if t['transaction_type'] == 'SELL')
    jml_beli    = sum(1 for t in transaction_history if t['transaction_type'] == 'BUY')
    jml_jual    = sum(1 for t in transaction_history if t['transaction_type'] == 'SELL')

    print()
    print(tabulate(
        [
            ["Total Transactions", len(transaction_history)],
            ["BUY Orders",         f"{jml_beli} transactions  ({format_rupiah(total_beli)})"],
            ["SELL Orders",        f"{jml_jual} transactions  ({format_rupiah(total_jual)})"],
        ],
        headers=["  TRANSACTION SUMMARY", ""],
        tablefmt="simple_outline",
        colalign=("left", "right")
    ))

# Analytics Dashboard

def analytics_dashboard():
    if len(portfolio) == 0:
        print_info("Portfolio is empty. No data to display.")
        return

    total_market_value = 0
    total_cost         = 0
    best_asset         = ""
    worst_asset        = ""
    best_profit        = -999999999999
    worst_profit       = 999999999999
    category_breakdown = {}

    for item in portfolio:

        market_value = item['quantity'] * item['market_price']
        cost         = item['quantity'] * item['buy_price']
        profit       = market_value - cost

        total_market_value += market_value
        total_cost         += cost

        if profit > best_profit:
            best_profit = profit
            best_asset  = item['asset_name']

        if profit < worst_profit:
            worst_profit = profit
            worst_asset  = item['asset_name']

        category = item['category']

        if category not in category_breakdown:
            category_breakdown[category] = {
                'market_value' : 0,
                'profit_loss'  : 0,
                'count'        : 0
            }

        category_breakdown[category]['market_value'] += market_value
        category_breakdown[category]['profit_loss']  += profit
        category_breakdown[category]['count']        += 1

    total_pl = total_market_value - total_cost

    if total_cost > 0:
        roi = (total_pl / total_cost) * 100
    else:
        roi = 0

    pl_label  = f"+{format_rupiah(total_pl)}" if total_pl >= 0 else format_rupiah(total_pl)
    roi_label = f"+{roi:.2f}%" if roi >= 0 else f"{roi:.2f}%"

    category_data = []

    for category, data in category_breakdown.items():

        persen    = (data['market_value'] / total_market_value) * 100
        pl_cat    = f"+{format_rupiah(data['profit_loss'])}" if data['profit_loss'] >= 0 else format_rupiah(data['profit_loss'])

        category_data.append([
            category,
            data['count'],
            format_rupiah(data['market_value']),
            f"{persen:.2f}%",
            pl_cat
        ])

        category_data.sort(key=lambda x: float(x[3].replace('%', '')), reverse=True)

    tabel_category = tabulate(
        category_data,
        headers=["Category", "Assets", "Market Value", "Allocation %", "P/L"],
        tablefmt="fancy_grid"
    )

    lebar_tabel = len(tabel_category.splitlines()[0])
  
    print(f"\n{'═' * lebar_tabel}")
    print("PORTFOLIO ANALYTICS".center(lebar_tabel))
    print(f"{'═' * lebar_tabel}")
    print()
    print_summary_box([
        ("Total Portfolio Value",  format_rupiah(total_market_value)),
        ("Total Investment",       format_rupiah(total_cost)),
        ("Unrealized P/L",         pl_label),
        ("Return on Investment",   roi_label),
        ("Best Performing Asset",  best_asset),
        ("Worst Performing Asset", worst_asset),
        ("Total Assets",           str(len(portfolio))),
    ], title="PERFORMANCE SUMMARY", width=lebar_tabel - 2)

    # Tabel category breakdown
    print()
    print(tabel_category)


# Search Asset

def search_asset():
    print_header("Search Asset")

    asset_id = input("\n  Enter Asset ID : ").upper()
    idx = cari_asset(asset_id)

    if idx == -1:
        print_error(f"Asset ID '{asset_id}' not found in portfolio.")
        return

    asset        = portfolio[idx]
    market_value = asset['quantity'] * asset['market_price']
    investasi    = asset['quantity'] * asset['buy_price']
    profit_loss  = market_value - investasi
    pl_pct       = (profit_loss / investasi * 100) if investasi > 0 else 0
    pl_label     = f"+{format_rupiah(profit_loss)}" if profit_loss >= 0 else format_rupiah(profit_loss)
    pct_label    = f"+{pl_pct:.2f}%" if pl_pct >= 0 else f"{pl_pct:.2f}%"

    print()
    print_summary_box([
        ("Asset ID",         asset['asset_id']),
        ("Asset Name",       asset['asset_name']),
        ("Category",         asset['category']),
        ("Status",           asset['status']),
        ("Purchase Date",    asset['purchase_date']),
        ("Quantity",         f"{asset['quantity']:.4f}"),
        ("Average Cost",     format_rupiah(asset['buy_price'])),
        ("Current Price",    format_rupiah(asset['market_price'])),
        ("Total Investment", format_rupiah(investasi)),
        ("Market Value",     format_rupiah(market_value)),
        ("Unrealized P/L",   f"{pl_label}  ({pct_label})"),
    ], title="ASSET DETAIL", width=LEBAR - 2)         

# Filter by Category

def filter_by_category():
    print_header("Filter by Category")

    categories = []

    for item in portfolio:
        if item['category'] not in categories:
            categories.append(item['category'])

    if not categories:
        print_info("No categories found in portfolio.")
        return

    print()
    print(tabulate(
        [[i + 1, cat] for i, cat in enumerate(categories)],
        headers=["#", "Available Categories"],
        tablefmt="simple_outline",
        colalign=("center", "left")
    ))

    pilihan = input(f"\n  Select Category (1-{len(categories)}) : ")

    if not pilihan.isdigit():
        print_error("Please enter a valid number.")
        return

    idx_pilihan = int(pilihan) - 1
    
    if not (0 <= idx_pilihan < len(categories)):
        print_error(f"Please select between 1 and {len(categories)}.")
        return

    selected_category = categories[idx_pilihan]

    data        = []
    total_value  = 0
    total_profit = 0

    for asset in portfolio:
        if asset['category'] == selected_category:
            market_value = asset['quantity'] * asset['market_price']
            investasi    = asset['quantity'] * asset['buy_price']
            profit_loss  = market_value - investasi
            pl_label     = f"+{format_rupiah(profit_loss)}" if profit_loss >= 0 else format_rupiah(profit_loss)

            total_value  += market_value
            total_profit += profit_loss

            data.append([
                asset['asset_id'],
                asset['asset_name'],
                asset['status'],
                f"{asset['quantity']:.4f}",
                format_rupiah(market_value),
                pl_label
            ])

    tabel_filter = tabulate(
        data,
        headers=["Asset ID", "Asset Name", "Status", "Quantity", "Market Value", "Unrealized P/L"],
        tablefmt="fancy_grid"
    )

    lebar_tabel = len(tabel_filter.splitlines()[0])

    print(f"\n{'═' * lebar_tabel}")
    print(f"Category : {selected_category}  ({len(data)} assets)".upper().center(lebar_tabel))
    print(f"{'═' * lebar_tabel}")

    print(tabel_filter)

    total_pl_label = f"+{format_rupiah(total_profit)}" if total_profit >= 0 else format_rupiah(total_profit)

    print()
    print_summary_box([
        ("Category Total Value", format_rupiah(total_value)),
        ("Category Total P/L",   total_pl_label),
    ], title="CATEGORY SUMMARY", width=lebar_tabel - 2)


# Sort Porfolio

def sort_asset():
    print_header("Sort Portfolio")
    while True:
        print()
        print(tabulate(
            [
                ["1", "Market Value   — Low to High"],
                ["2", "Market Value   — High to Low"],
                ["3", "Profit / Loss  — Low to High"],
                ["4", "Profit / Loss  — High to Low"],
                ["0", "Back to Main Menu"],
            ],
            headers=["#", "  SORT OPTIONS"],
            tablefmt="simple_outline",
            colalign=("center", "left")
        ))

        pilihan = input("\n  Select sorting method : ")

        if pilihan == '0':
            break

        data_sort = portfolio.copy()

        if pilihan == '1':
            data_sort.sort(key=lambda x: x['quantity'] * x['market_price'])
        elif pilihan == '2':
            data_sort.sort(key=lambda x: x['quantity'] * x['market_price'], reverse=True)
        elif pilihan == '3':
            data_sort.sort(key=lambda x: (x['quantity'] * x['market_price']) - (x['quantity'] * x['buy_price']))
        elif pilihan == '4':
            data_sort.sort(key=lambda x: (x['quantity'] * x['market_price']) - (x['quantity'] * x['buy_price']), reverse=True)
        else:
            print_error("Invalid option. Select 0–4.")
            continue

        data = []

        for item in data_sort:
            market_value = item['quantity'] * item['market_price']
            investasi    = item['quantity'] * item['buy_price']
            profit_loss  = market_value - investasi
            pl_label     = f"+{format_rupiah(profit_loss)}" if profit_loss >= 0 else format_rupiah(profit_loss)

            data.append([
                item['asset_id'],
                item['asset_name'],
                item['category'],
                f"{item['quantity']:.4f}",
                format_rupiah(market_value),
                pl_label
            ])

        print()
        print(tabulate(
            data,
            headers=["Asset ID", "Asset Name", "Category", "Quantity", "Market Value", "Unrealized P/L"],
            tablefmt="fancy_grid"
        ))


# Main Menu

def main_menu():
    while True:
        print(f'''
{"═" * LEBAR}
  {APP_NAME.center(LEBAR - 2)}
  {APP_SLOGAN.center(LEBAR - 2)}
{"═" * LEBAR}

  PORTFOLIO MANAGEMENT          ANALYTICS
  ─────────────────────         ─────────────────────
  [1]  View Portfolio           [7]  Performance Summary
  [2]  Add Asset                [8]  Search Asset
  [3]  Update Asset             [9]  Filter by Category
  [4]  Delete Asset             [10] Sort Portfolio

  TRANSACTION                   SYSTEM
  ─────────────────────         ─────────────────────
  [5]  Buy / Sell Asset         [11] Exit
  [6]  Transaction History

{"─" * LEBAR}''')
        pilihan = input("\n  Select Menu [1-11] : ")

        if pilihan == '1':
            tampilkan_portfolio()
            back_menu()
        elif pilihan == '2':
            tambah_asset()
            back_menu()
        elif pilihan == '3':
            update_asset()
            back_menu()
        elif pilihan == '4':
            delete_asset()
            back_menu()
        elif pilihan == '5':
            transaksi_asset()
            back_menu()
        elif pilihan == '6':
            tampilkan_transaksi()
            back_menu()
        elif pilihan == '7':
            analytics_dashboard()
            back_menu()
        elif pilihan == '8':
            search_asset()
            back_menu()
        elif pilihan == '9':
            filter_by_category()
            back_menu()
        elif pilihan == '10':
            sort_asset()
            back_menu()
        elif pilihan == '11':
            print(f'''
{"─" * LEBAR}
  {"Logging out from " + APP_NAME}
  {"Thank you for using AssetHub. Goodbye!"}
{"─" * LEBAR}
''')
            return
        else:
            print_error("Invalid menu selection. Please enter 1–11.")


# Program Start

if __name__ == '__main__':
    while True:
        if login():
            main_menu()       # kembali ke sini setelah Exit di main menu
        else:
            break             # akses ditolak (3x salah PIN) → terminate
    print("\n  Program terminated.")

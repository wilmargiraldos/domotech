import csv
import json
import argparse
from typing import Optional
from .repositories import OrderRepository
from .session import SessionLocal


def export_user_orders_csv(session, user_id: int, out_path: str) -> None:
    orr = OrderRepository(session)
    orders = orr.get_user_orders(user_id)

    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['order_id', 'created_at', 'status', 'total'])
        for o in orders:
            writer.writerow([o.id, o.created_at.isoformat(), o.status, o.total])


def export_all_orders_json(session, out_path: str) -> None:
    orr = OrderRepository(session)
    orders = orr.get_all_orders()

    out = []
    for o in orders:
        items = []
        for it in o.items:
            items.append({
                'product_id': it.product_id,
                'qty': it.qty,
                'unit_price': it.unit_price,
            })
        out.append({
            'order_id': o.id,
            'user_id': o.user_id,
            'created_at': o.created_at.isoformat(),
            'status': o.status,
            'total': o.total,
            'items': items,
        })

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)


def main(argv: Optional[list] = None) -> None:
    parser = argparse.ArgumentParser(description='Export orders reports')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--user-csv', nargs=2, metavar=('USER_ID', 'OUT_CSV'), help='Export user orders to CSV')
    group.add_argument('--all-json', metavar='OUT_JSON', help='Export all orders to JSON')
    args = parser.parse_args(argv)

    with SessionLocal() as session:
        if args.user_csv:
            user_id = int(args.user_csv[0])
            out = args.user_csv[1]
            export_user_orders_csv(session, user_id, out)
            print(f'Wrote user orders CSV to {out}')
        elif args.all_json:
            out = args.all_json
            export_all_orders_json(session, out)
            print(f'Wrote all orders JSON to {out}')


if __name__ == '__main__':
    main()

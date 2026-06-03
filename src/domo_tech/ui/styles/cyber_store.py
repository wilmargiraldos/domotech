"""Cyber Punk for Online Store CSS styles."""

# Sections
CYBER_STORE_CSS = """
/* ════════════ BASE ════════════ */
Screen {
    background: #05050f;
}

/* ════════════ LOGIN ════════════ */
LoginScreen {
    align: center middle;
}

#login-box {
    width: 64;
    height: auto;
    border: heavy #ff00ff;
    background: #0a0a1f;
    padding: 1 3;
}

.login-box-wide {
    width: 86;
}

#logo {
    color: #ff00ff;
    text-align: center;
    margin-bottom: 1;
    text-style: bold;
}

#login-tag {
    color: #00ffff;
    text-align: center;
    margin-bottom: 2;
}

.field-label {
    color: #666688;
    margin-top: 1;
    margin-bottom: 0;
    padding-left: 1;
}

Input {
    background: #0d0d2b;
    color: #00ff88;
    border: tall #ff00ff 40%;
    margin-bottom: 0;
}

Input:focus {
    border: tall #ff00ff;
    background: #111133;
}

#btn-login {
    margin-top: 0;
    background: #ff00ff 20%;
    color: #ff00ff;
    border: tall #ff00ff;
    width: 1fr;
    text-style: bold;
}

#btn-login:hover {
    background: #ff00ff 40%;
    color: #ffffff;
}

#btn-register {
    margin-top: 0;
    background: #00ffff 10%;
    color: #00ffff;
    border: tall #00ffff 60%;
    width: 1fr;
}

#btn-register:hover {
    background: #00ffff 30%;
    color: #ffffff;
}

#login-error {
    color: #ff3333;
    text-align: center;
    height: 1;
    margin-top: 1;
}

#login-actions {
    margin-top: 2;
    height: auto;
}

#login-actions Button {
    height: 3;
}

#btn-login {
    margin-right: 1;
}

#btn-register {
    margin-left: 1;
}

#login-footer-text {
    color: #2a2a44;
    text-align: center;
    margin-top: 1;
}

/* ════════════ ADMIN ════════════ */
AdminScreen {
    align: left top;
    background: #05050f;
}

#admin-shell {
    width: 100%;
    height: 100%;
    padding: 0 1;
}

#admin-header {
    height: 1;
    background: #0a0a1f;
    border-bottom: heavy #00ffff;
    padding: 0 1;
    align: left middle;
}

#admin-title {
    color: #00ffff;
    text-style: bold;
    width: 1fr;
    min-width: 0;
}

#admin-user {
    color: #ff00ff;
    width: auto;
    min-width: 22;
    content-align: right middle;
}

#admin-nav {
    height: 3;
    margin-top: 0;
}

#admin-nav Button {
    width: 1fr;
    margin-right: 1;
}

#admin-nav Button:last-child {
    margin-right: 0;
}

#admin-kpis {
    height: 4;
    margin-top: 0;
}

#admin-kpis Static {
    width: 1fr;
    margin-right: 1;
    padding: 0 1;
    border: solid #1a1a3a;
    background: #0a0a1f;
    color: #cccccc;
}

#admin-kpis Static:last-child {
    margin-right: 0;
}

#admin-status {
    margin-top: 0;
    color: #00ff88;
    text-align: center;
    height: 1;
}

#admin-content {
    height: 1fr;
    min-height: 0;
    margin-top: 0;
    padding: 0 1;
    background: #0a0a1f;
    border: heavy #1a1a3a;
}

#admin-main {
    height: 1fr;
    min-height: 0;
}

#admin-overview-section,
#admin-users-section,
#admin-products-section,
#admin-sales-section,
#admin-logs-section {
    height: 1fr;
    min-height: 0;
    padding: 0 1;
}

#admin-status-bar {
    margin-top: 0;
    height: 2;
    padding: 0 1;
    align: left middle;
    border-top: solid #00ffff 25%;
    background: #05050f;
}

#admin-help-text {
    color: #666688;
    width: 3fr;
    min-width: 0;
}

#admin-op-status {
    color: #00ff88;
    width: 2fr;
    min-width: 0;
    content-align: left middle;
}

#admin-clock {
    color: #00ffff;
    width: auto;
    min-width: 20;
    content-align: right middle;
}

.admin-section-title {
    color: #ff00ff;
    text-style: bold;
    margin-bottom: 1;
}

.admin-field-label {
    color: #666688;
    margin-top: 1;
    margin-bottom: 0;
}

#admin-users-layout,
#admin-products-layout {
    height: auto;
    min-height: 0;
}

#admin-users-table-box,
#admin-products-table-box {
    width: 2fr;
    margin-right: 1;
}

#admin-user-editor,
#admin-product-editor {
    width: 3fr;
    background: #05050f;
    border: solid #1a1a3a;
    padding: 1 2;
}

#admin-users-table,
#admin-products-table {
    height: 14;
    margin-bottom: 1;
}

#admin-users-hint,
#admin-products-hint {
    color: #888899;
    margin-bottom: 1;
}

#admin-user-editor Input,
#admin-product-editor Input {
    width: 100%;
    margin-bottom: 0;
}

#admin-user-editor Button,
#admin-product-editor Button {
    margin-top: 1;
    width: 100%;
}

#admin-low-stock,
#admin-sales-overview,
#admin-overview-text,
#admin-sales-chart,
#admin-top-products-chart,
#admin-inventory-chart,
#admin-events-chart,
#admin-order-status-chart,
#admin-revenue-chart {
    margin-top: 0;
    color: #cccccc;
    background: #05050f;
    border: solid #1a1a2e;
    padding: 1 2;
}

#admin-log-scroll {
    height: auto;
    min-height: 10;
    background: #05050f;
    border: solid #1a1a2e;
    padding: 1 2;
}

RegisterModal {
    align: center middle;
    background: #000008 80%;
}

#register-box {
    width: 58;
    height: auto;
    border: heavy #00ffff;
    background: #0a0a1f;
    padding: 2 3;
}

#register-title {
    color: #00ffff;
    text-align: center;
    text-style: bold;
    margin-bottom: 1;
}

#btn-register-confirm {
    margin-top: 2;
    background: #00ff88 15%;
    color: #00ff88;
    border: tall #00ff88;
    width: 100%;
    text-style: bold;
}

#btn-register-confirm:hover {
    background: #00ff88 35%;
    color: #ffffff;
}

#btn-register-cancel {
    margin-top: 1;
    background: #333344;
    color: #888899;
    border: tall #444455;
    width: 100%;
}

#btn-register-cancel:hover {
    background: #444455;
    color: #ffffff;
}

#register-error {
    color: #ffaa00;
    text-align: center;
    height: 1;
    margin-top: 1;
}

/* ════════════ STORE ════════════ */
#store-header {
    height: 2;
    background: #0a0a1f;
    border-bottom: heavy #ff00ff;
    padding: 0 2;
    align: left middle;
}

#store-title {
    color: #ff00ff;
    text-style: bold;
    width: 1fr;
    min-width: 0;
    content-align: left middle;
}

#user-badge {
    color: #00ffff;
    width: auto;
    content-align: right middle;
    padding-right: 2;
}

#main-area {
    height: 1fr;
    min-height: 0;
}

/* ── Products ── */
#products-panel {
    width: 2fr;
    border-right: heavy #ff00ff 40%;
    min-height: 0;
}

#prod-header {
    height: 4;
    background: #ff00ff 12%;
    border-bottom: solid #ff00ff 40%;
    padding: 0 2;
    align: left middle;
}

#prod-header-title {
    color: #ff00ff;
    text-style: bold;
    width: 1fr;
    min-width: 0;
}

#filter-input {
    width: 30;
    height: 3;
    background: #0a0a1f;
    color: #ff00ff;
    border: solid #ff00ff 50%;
    padding: 0 1;
}

#filter-input:focus {
    border: solid #ff00ff;
    color: #00ff88;
    background: #111133;
}

#products-table {
    height: 1fr;
    background: #05050f;
    min-height: 0;
}

DataTable {
    background: #05050f;
    color: #cccccc;
}

DataTable > .datatable--header {
    background: #0a0a2a;
    color: #ff00ff;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: #ff00ff 25%;
    color: #ffffff;
    text-style: bold;
}

DataTable > .datatable--hover {
    background: #ff00ff 10%;
}

#prod-actions {
    height: auto;
    background: #0a0a1f;
    border-top: solid #1a1a3a;
    padding: 0 2 1 2;
    align: left middle;
}

#prod-actions Button {
    height: 3;
}

#btn-add {
    background: #00ff88 15%;
    color: #00ff88;
    border: tall #00ff88;
    margin-right: 2;
    text-style: bold;
}

#btn-add:hover { background: #00ff88 35%; }

#btn-logout {
    background: #333344;
    color: #666677;
    border: tall #444455;
}

#btn-logout:hover {
    background: #444455;
    color: #aaaacc;
}

/* ── Cart ── */
#cart-panel {
    width: 1fr;
    background: #080818;
    min-height: 0;
}

#cart-header {
    height: 2;
    background: #00ffff 12%;
    border-bottom: solid #00ffff 40%;
    padding: 0 2;
    align: left middle;
}

#cart-header-title {
    color: #00ffff;
    text-style: bold;
    width: 1fr;
}

#cart-count {
    color: #00ff88;
    text-style: bold;
}

#cart-items {
    height: 1fr;
    padding: 1 0;
    overflow-y: auto;
    min-height: 0;
}

.cart-item {
    height: 3;
    padding: 0 2;
    border-bottom: solid #1a1a2e;
    align: left middle;
}

.cart-item:hover {
    background: #00ffff 05%;
}

.ci-name {
    color: #cccccc;
    width: 1fr;
}

.ci-qty {
    color: #888899;
    width: 6;
    content-align: center middle;
}

.ci-price {
    color: #ffff44;
    width: 10;
    content-align: right middle;
    text-style: bold;
}

#cart-empty {
    color: #333355;
    text-align: center;
    padding-top: 4;
}

#cart-footer {
    height: auto;
    background: #0a0a1f;
    border-top: heavy #00ffff;
    padding: 0 2 1 2;
}

#total-row {
    align: left middle;
    height: 1;
    margin-bottom: 0;
    width: 100%;
}

#total-label {
    color: #555577;
    width: auto;
    min-width: 7;
}

#total-value {
    color: #00ff88;
    text-style: bold;
    width: 1fr;
    content-align: right middle;
}

#btn-checkout {
    background: #00ffff 20%;
    color: #00ffff;
    border: tall #00ffff;
    width: 100%;
    text-style: bold;
}

#btn-checkout:hover { background: #00ffff 40%; color: #ffffff; }

#btn-clear {
    background: #ff3333 10%;
    color: #ff3333;
    border: tall #ff3333;
    width: 100%;
    margin-top: 1;
}

#btn-clear:hover { background: #ff3333 30%; }

/* ── Status bar ── */
#status-bar {
    height: 2;
    background: #0a0a1f;
    border-top: solid #ff00ff 25%;
    padding: 0 2;
    align: left middle;
}

#status-text {
    color: #00ff88;
    width: 1fr;
    min-width: 0;
    content-align: left middle;
}

#clock {
    color: #666688;
    width: 8;
    content-align: right middle;
}

#status-bar Static {
    height: 1;
}

/* ════════════ CHECKOUT MODAL ════════════ */
CheckoutModal {
    align: center middle;
    background: #000008 80%;
}

#checkout-box {
    width: 56;
    height: auto;
    border: heavy #00ffff;
    background: #0a0a1f;
    padding: 2 3;
}

#checkout-title {
    color: #00ffff;
    text-style: bold;
    text-align: center;
    margin-bottom: 1;
}

#checkout-divider {
    color: #1a1a3a;
    text-align: center;
    margin-bottom: 1;
}

.checkout-row {
    height: 2;
    align: left middle;
    border-bottom: solid #111128;
}

.co-name { color: #aaaacc; width: 1fr; }
.co-qty  { color: #666688; width: 5; content-align: center middle; }
.co-sub  { color: #ffff44; width: 12; content-align: right middle; }

#checkout-total-row {
    height: 2;
    align: left middle;
    margin-top: 1;
    border-top: solid #00ffff 40%;
    padding-top: 1;
}

#co-total-label { color: #555577; width: 1fr; text-style: bold; }
#co-total-val   { color: #00ff88; text-style: bold; }

#checkout-warn {
    color: #ffaa00;
    text-align: center;
    margin-top: 1;
}

#checkout-btns {
    margin-top: 2;
    align: center middle;
    height: 3;
}

#btn-confirm {
    background: #00ff88 20%;
    color: #00ff88;
    border: tall #00ff88;
    width: 1fr;
    margin-right: 2;
    text-style: bold;
}

#btn-confirm:hover { background: #00ff88 40%; color: #000; }

#btn-cancel {
    background: #ff3333 10%;
    color: #ff3333;
    border: tall #ff3333;
    width: 1fr;
}

#btn-cancel:hover { background: #ff3333 30%; }

/* ════════════ PRODUCT DETAIL MODAL ════════════ */
ProductDetailModal {
    align: center middle;
    background: #000008 80%;
}

#product-detail-box {
    width: 76;
    height: 28;
    border: heavy #ff00ff;
    background: #0a0a1f;
    padding: 1 2;
}

#product-detail-title {
    color: #ff00ff;
    text-style: bold;
    text-align: center;
    height: 1;
    margin-bottom: 1;
}

#product-detail-name {
    color: #00ffff;
    text-style: bold;
    height: 2;
    content-align: center middle;
}

#product-detail-meta {
    height: 3;
    border-top: solid #1a1a3a;
    border-bottom: solid #1a1a3a;
    align: center middle;
}

.pd-meta {
    color: #00ff88;
    width: 1fr;
    content-align: center middle;
}

#product-detail-body {
    height: 1fr;
    min-height: 0;
    padding: 1 1;
    overflow-y: auto;
}

#pd-desc {
    color: #cccccc;
    margin-bottom: 1;
}

.pd-section {
    color: #ff00ff;
    text-style: bold;
    margin-top: 1;
    margin-bottom: 1;
}

.pd-line {
    color: #aaaacc;
    margin-bottom: 1;
}

#btn-detail-close {
    background: #ff00ff 15%;
    color: #ff00ff;
    border: tall #ff00ff;
    width: 100%;
    height: 3;
    text-style: bold;
}

#btn-detail-close:hover {
    background: #ff00ff 35%;
    color: #ffffff;
}

/* ════════════ HELP MODAL ════════════ */
HelpModal {
    align: center middle;
    background: #000008 80%;
}

#help-box {
    width: 82;
    height: 32;
    border: heavy #00ffff;
    background: #0a0a1f;
    padding: 1 2;
}

#help-title {
    color: #00ffff;
    text-style: bold;
    text-align: center;
    height: 1;
    margin-bottom: 1;
}

#help-search {
    height: 3;
    width: 100%;
    margin-bottom: 1;
    border: solid #00ffff 60%;
    color: #00ff88;
}

#help-search:focus {
    border: solid #00ffff;
    background: #111133;
}

#help-results {
    height: 1fr;
    min-height: 0;
    overflow-y: auto;
    padding: 0 1;
}

.help-entry {
    color: #cccccc;
    border-bottom: solid #1a1a3a;
    padding: 1 0;
    margin-bottom: 1;
}

.help-empty {
    color: #ffaa00;
    content-align: center middle;
    height: 5;
}

#btn-help-close {
    background: #00ffff 15%;
    color: #00ffff;
    border: tall #00ffff;
    width: 100%;
    height: 3;
    text-style: bold;
    margin-top: 1;
}

#btn-help-close:hover {
    background: #00ffff 35%;
    color: #ffffff;
}

/* ════════════ SUCCESS MODAL ════════════ */
SuccessModal {
    align: center middle;
    background: #000008 80%;
}

#success-box {
    width: 50;
    height: auto;
    border: heavy #00ff88;
    background: #0a1a0a;
    padding: 3 4;
    align: center middle;
}

#success-icon {
    color: #00ff88;
    text-align: center;
    text-style: bold;
    margin-bottom: 1;
}

#success-msg {
    color: #cccccc;
    text-align: center;
    margin-bottom: 2;
}

#success-order {
    color: #00ffff;
    text-align: center;
    text-style: bold;
    margin-bottom: 2;
}

#btn-ok {
    background: #00ff88 20%;
    color: #00ff88;
    border: tall #00ff88;
    width: 100%;
    text-style: bold;
}

#btn-ok:hover { background: #00ff88 40%; }
"""

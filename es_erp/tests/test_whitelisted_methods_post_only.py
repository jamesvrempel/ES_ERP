import importlib

import frappe
from frappe.tests.utils import FrappeTestCase

POST_ONLY_METHODS = (
	"es_erp.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.update_bank_transaction",
	"es_erp.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_journal_entry_bts",
	"es_erp.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.create_payment_entry_bts",
	"es_erp.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.reconcile_vouchers",
	"es_erp.accounts.doctype.bank_transaction.bank_transaction_upload.create_bank_entries",
	"es_erp.accounts.doctype.bisect_accounting_statements.bisect_accounting_statements.BisectAccountingStatements.bisect_left",
	"es_erp.accounts.doctype.bisect_accounting_statements.bisect_accounting_statements.BisectAccountingStatements.bisect_right",
	"es_erp.accounts.doctype.bisect_accounting_statements.bisect_accounting_statements.BisectAccountingStatements.move_up",
	"es_erp.accounts.doctype.cheque_print_template.cheque_print_template.create_or_update_cheque_print_format",
	"es_erp.accounts.doctype.payment_request.payment_request.make_payment_request",
	"es_erp.assets.doctype.location.location.add_node",
	"es_erp.buying.doctype.request_for_quotation.request_for_quotation.create_supplier_quotation",
	"es_erp.controllers.stock_controller.make_quality_inspections",
	"es_erp.crm.doctype.lead.lead.make_lead_from_communication",
	"es_erp.crm.doctype.opportunity.opportunity.set_multiple_status",
	"es_erp.crm.doctype.opportunity.opportunity.make_opportunity_from_communication",
	"es_erp.es_erp_integrations.doctype.plaid_settings.plaid_settings.add_institution",
	"es_erp.es_erp_integrations.doctype.plaid_settings.plaid_settings.add_bank_accounts",
	"es_erp.manufacturing.doctype.work_order.work_order.set_work_order_ops",
	"es_erp.manufacturing.doctype.workstation.workstation.Workstation.start_job",
	"es_erp.manufacturing.doctype.workstation.workstation.Workstation.complete_job",
	"es_erp.projects.doctype.project.project.create_duplicate_project",
	"es_erp.projects.doctype.project.project.set_project_status",
	"es_erp.projects.doctype.task.task.set_multiple_status",
	"es_erp.projects.doctype.task.task.add_node",
	"es_erp.projects.doctype.task.task.add_multiple_tasks",
	"es_erp.quality_management.doctype.quality_procedure.quality_procedure.add_node",
	"es_erp.selling.doctype.customer.customer.Customer.get_customer_group_details",
	"es_erp.selling.doctype.sales_order.sales_order.make_work_orders",
	"es_erp.selling.page.point_of_sale.point_of_sale.create_opening_voucher",
	"es_erp.selling.page.point_of_sale.point_of_sale.set_customer_info",
	"es_erp.setup.doctype.company.company.add_node",
	"es_erp.setup.doctype.department.department.add_node",
	"es_erp.setup.doctype.employee.employee.create_user",
	"es_erp.stock.doctype.batch.batch.split_batch",
	"es_erp.stock.doctype.material_request.material_request.raise_work_orders",
	"es_erp.stock.doctype.warehouse.warehouse.add_node",
	"es_erp.stock.report.stock_and_account_value_comparison.stock_and_account_value_comparison.create_reposting_entries",
	"es_erp.stock.report.stock_ledger_invariant_check.stock_ledger_invariant_check.create_reposting_entries",
	"es_erp.subcontracting.doctype.subcontracting_receipt.subcontracting_receipt.make_purchase_receipt",
	"es_erp.support.doctype.issue.issue.make_issue_from_communication",
	"es_erp.support.doctype.service_level_agreement.service_level_agreement.reset_service_level_agreement",
	"es_erp.telephony.doctype.call_log.call_log.add_call_summary_and_call_type",
)


class TestWhitelistedMethodsPostOnly(FrappeTestCase):
	def test_state_changing_methods_accept_only_post(self):
		for path in POST_ONLY_METHODS:
			with self.subTest(path=path):
				method = resolve(path)
				self.assertIn(method, frappe.whitelisted)
				self.assertEqual(frappe.allowed_http_methods_for_whitelisted_func.get(method), ["POST"])


def resolve(path: str):
	"""Resolve a dotted path to a module function or a class method."""
	module_path, _, attribute = path.rpartition(".")
	try:
		return getattr(importlib.import_module(module_path), attribute)
	except ModuleNotFoundError:
		module_path, _, class_name = module_path.rpartition(".")
		return getattr(getattr(importlib.import_module(module_path), class_name), attribute)

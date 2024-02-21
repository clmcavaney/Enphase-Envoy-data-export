import logging

from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_float import Property_Float
from homie.node.property.property_integer import Property_Integer
from homie.node.property.property_string import Property_String

logger = logging.getLogger(__name__)

class Device_Enphase_Envoy(Device_Base):
	def __init__(
		self, device_id=None, name=None, homie_settings=None, mqtt_settings=None
	):

		super().__init__(device_id, name, homie_settings, mqtt_settings)

		# Add 3 nodes - details, production, consumption
		# Details
		node = Node_Base(self, id='details', name='Details', type_='Envoy details')
		self.add_node(node)
		node.add_property(Property_Integer(node, name='serial_number', id='sn', settable=False))
		node.add_property(Property_String(node, name='output_date', id='date', unit='YYYYMMDD', settable=False))
		node.add_property(Property_String(node, name='output_time', id='time', unit='HH:MM', settable=False))

		# Production
		node = Node_Base(self, id='production', name='Production', type_='Production data')
		self.add_node(node)
		node.add_property(Property_Float(node, name='production energy today', id='p-e-wh-today', unit='Wh', settable=False))
		node.add_property(Property_Float(node, name='production energy lifetime', id='p-e-wh-lifetime', unit='Wh', settable=False))
		node.add_property(Property_Float(node, name='production power now', id='p-p-w-now', unit='W', settable=False))
		node.add_property(Property_Float(node, name='production voltage RMS', id='p-v-rms', unit='V', settable=False))
		node.add_property(Property_Float(node, name='production power factor', id='p-pwr-f', unit='PF', settable=False))

		# Consumption
		node = Node_Base(self, id='consumption', name='Consumption', type_='Consumption data')
		self.add_node(node)
		node.add_property(Property_Float(node, name='consumption energy today', id='c-e-wh-today', unit='Wh', settable=False))
		node.add_property(Property_Float(node, name='consumption energy lifetime', id='c-e-wh-lifetime', unit='Wh', settable=False))
		node.add_property(Property_Float(node, name='consumption power now', id='c-p-w-now', unit='W', settable=False))
		node.add_property(Property_Float(node, name='consumption voltage RMS', id='c-v-rms', unit='V', settable=False))
		node.add_property(Property_Float(node, name='consumption power factor', id='c-pwr-f', unit='PF', settable=False))

		self.start()

	def update_details(self, serial_number, output_date, output_time):
		details_node = self.get_node('details')

		details_node.get_property('sn').value = serial_number
		details_node.get_property('date').value = output_date
		details_node.get_property('time').value = output_time

	def update_production(self, e_whToday, e_whLifetime, p_wNow, p_v_rms, p_pwr_f):
		production_node = self.get_node('production')

		production_node.get_property('p-e-wh-today').value = e_whToday;
		production_node.get_property('p-e-wh-lifetime').value = e_whLifetime;
		production_node.get_property('p-p-w-now').value = p_wNow;
		production_node.get_property('p-v-rms').value = p_v_rms;
		production_node.get_property('p-pwr-f').value = p_pwr_f;

	def update_consumption(self, e_whToday, e_whLifetime, p_wNow, p_v_rms, p_pwr_f):
		consumption_node = self.get_node('consumption')

		consumption_node.get_property('c-e-wh-today').value = e_whToday;
		consumption_node.get_property('c-e-wh-lifetime').value = e_whLifetime;
		consumption_node.get_property('c-p-w-now').value = p_wNow;
		consumption_node.get_property('c-v-rms').value = p_v_rms;
		consumption_node.get_property('c-pwr-f').value = p_pwr_f;

# vim:expandtab
# END OF FILE

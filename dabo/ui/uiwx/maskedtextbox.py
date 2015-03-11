# -*- coding: utf-8 -*-
import datetime
import wx
import wx.lib.masked as masked
import dabo
from dabo.ui import makeDynamicProperty
from dabo.dLocalize import _
from . import textboxmixin as tbm



class dMaskedTextBox(tbm.dTextBoxMixin, masked.TextCtrl):
	"""
	This is a specialized textbox class that supports a Mask property. The
	mask determines what characters are allowed in the textbox, and can also
	include formatting characters that are not part of the control's Value.
	"""
	_allowedInputCodes = ("_", "!", "^", "R", "r", "<", ">", ",", "-", "0", "D", "T", "F", "V", "S")
	_formatMap = {"phone-us": "USPHONEFULL",
			"phone-us-ext": "USPHONEFULLEXT",
			"ssn-us": "USSOCIALSEC",
			"zip-us": "USZIP",
			"zipplus4-us": "USZIPPLUS4",
			"date-us": "USDATEMMDDYYYY/",
			"date-us-slash": "USDATEMMDDYYYY/",
			"date-us-dash": "USDATEMMDDYYYY-",
			"date-us-yy": "USDATEMMDDYY/",
			"date-eu": "EUDATEDDMMYYYY.",
			"date-eu-slash": "EUDATEDDMMYYYY/",
			"date-eu-month": "EUDATEDDMMMYYYY.",
			"date-eu-month-slash": "EUDATEDDMMMYYYY/",
			"datetime-us": "USDATETIMEMMDDYYYY/HHMMSS",
			"datetime-us-dash": "USDATETIMEMMDDYYYY-HHMMSS",
			"datetime-us-24": "USDATE24HRTIMEMMDDYYYY/HHMMSS",
			"datetime-us-24-dash": "USDATE24HRTIMEMMDDYYYY-HHMMSS",
			"datetime-us-nosec": "USDATETIMEMMDDYYYY/HHMM",
			"datetime-us-dash-nosec": "USDATETIMEMMDDYYYY-HHMM",
			"datetime-us-24-nosec": "USDATE24HRTIMEMMDDYYYY/HHMM",
			"datetime-us-24-dash-nosec": "USDATE24HRTIMEMMDDYYYY-HHMM",
			"datetime-eu": "EUDATETIMEYYYYMMDD.HHMMSS",
			"datetime-eu-slash": "EUDATETIMEYYYYMMDD/HHMMSS",
			"datetime-eu-nosec": "EUDATETIMEYYYYMMDD.HHMM",
			"datetime-eu-slash-nosec": "EUDATETIMEYYYYMMDD/HHMM",
			"datetime-eu-24": "EUDATE24HRTIMEYYYYMMDD.HHMMSS",
			"datetime-eu-24-slash": "EUDATE24HRTIMEYYYYMMDD/HHMMSS",
			"datetime-eu-24-nosec": "EUDATE24HRTIMEYYYYMMDD.HHMM",
			"datetime-eu-24-slash-nosec": "EUDATE24HRTIMEYYYYMMDD/HHMM",
			"datetime-eu-dmy": "EUDATETIMEDDMMYYYY.HHMMSS",
			"datetime-eu-dmy-slash": "EUDATETIMEDDMMYYYY/HHMMSS",
			"datetime-eu-dmy-nosec": "EUDATETIMEDDMMYYYY.HHMM",
			"datetime-eu-dmy-slash-nosec": "EUDATETIMEDDMMYYYY/HHMM",
			"datetime-eu-dmy-24": "EUDATE24HRTIMEDDMMYYYY.HHMMSS",
			"datetime-eu-dmy-24-slash": "EUDATE24HRTIMEDDMMYYYY/HHMMSS",
			"datetime-eu-dmy-24-nosec": "EUDATE24HRTIMEDDMMYYYY.HHMM",
			"datetime-eu-dmy-24-slash-nosec": "EUDATE24HRTIMEDDMMYYYY/HHMM",
			"time": "TIMEHHMMSS",
			"time-nosec": "TIMEHHMM",
			"time-24": "24HRTIMEHHMMSS",
			"time-24-nosec": "24HRTIMEHHMM",
			"date-expiration": "EXPDATEMMYY",
			"email": "EMAIL",
			"ip": "IPADDR"}


	def __init__(self, parent, properties=None, attProperties=None, *args, **kwargs):
		self._baseClass = dMaskedTextBox
		self._valueMode = None
		self._mask = self._extractKey((properties, attProperties, kwargs), "Mask", "")
		self._format = self._extractKey((properties, attProperties, kwargs), "Format", "")
		self._validregex = self._extractKey((properties, attProperties, kwargs), "ValidRegex", "")
		self._inputCodes = self._uniqueCodes(self._extractKey((properties, attProperties, kwargs),
				"InputCodes", "_>"))
		kwargs["mask"] = self._mask
		kwargs["formatcodes"] = self._inputCodes
		kwargs["validRegex"] = self._validregex
		if self._format:
			code = self._formatMap.get(self._format.lower(), "")
			if code:
				kwargs["autoformat"] = code
				kwargs.pop("mask")
				kwargs.pop("formatcodes")
				kwargs.pop("validRegex")
		kwargs["useFixedWidthFont"] = False

		preClass = wx.lib.masked.TextCtrl
		tbm.dTextBoxMixin.__init__(self, preClass, parent, properties=properties,
				attProperties=attProperties, *args, **kwargs)


	def getFormats(cls):
		"""Return a list of available format codes."""
		return list(cls._formatMap.keys())
	getFormats = classmethod(getFormats)


	def _uniqueCodes(self, codes):
		"""
		Take a string and return the same string with any duplicate characters removed.
		The order of the characters is not preserved.
		"""
		return "".join(list(dict.fromkeys(codes).keys()))


	def _onWxHit(self, evt, *args, **kwargs):
		# This fixes wx masked control issue firing multiple EVT_TEXT events.
		if self._value != self.Value:
			super(dMaskedTextBox, self)._onWxHit(evt, *args, **kwargs)


	# property get/set functions
	def _getFormat(self):
		return self._format

	def _setFormat(self, val):
		if self._constructed():
			try:
				self.SetAutoformat(self._formatMap.get(val))
			except AttributeError:
				dabo.log.error(_("Invalid Format value: %s") % val)
				return
			self._format = val
			if not val:
				self.SetMask("")
				self.ClearValue()
		else:
			self._properties["Format"] = val


	def _getInputCodes(self):
		return self.GetFormatcodes()

	def _setInputCodes(self, val):
		if self._constructed():
			if self.GetAutoformat() and val:
				# Cannot have both a mask and a format
				dabo.log.error(_("Cannot set InputCodes when a Format has been set"))
			elif [cd for cd in val if cd not in self._allowedInputCodes]:
				# Illegal codes
				bad = "".join([cd for cd in val if cd not in self._allowedInputCodes])
				dabo.log.error(_("Invalid InputCodes: %s") % bad)
			else:
				val = self._uniqueCodes(val)
				self._inputCodes = val
				self.SetFormatcodes(val)
		else:
			self._properties["InputCodes"] = val


	def _getMask(self):
		return self.GetMask()

	def _setMask(self, val):
		if self._constructed():
			if self.GetAutoformat() and val:
				# Cannot have both a mask and a format
				raise RuntimeError(_("Cannot set a Mask when a Format has been set"))
			else:
				self._mask = val
				self.SetMask(val)
		else:
			self._properties["Mask"] = val


	def _getMaskedValue(self):
		return self.GetValue()


	def _getUnmaskedValue(self):
		return self.GetPlainValue()


	def _getValue(self):
		if self.ValueMode == "Masked":
			ret = self.GetValue()
		else:
			ret = self.GetPlainValue()
		return ret

	def _setValue(self, val):
		if val is None:
			val = ''
			
		super(dMaskedTextBox, self)._setValue(val)


	def _getValueMode(self):
		try:
			if self._valueMode.lower().startswith("m"):
				return "Masked"
			else:
				return "Unmasked"
		except (TypeError, AttributeError):
			return "Unmasked"

	def _setValueMode(self, val):
		if self._constructed():
			self._valueMode = val
		else:
			self._properties["ValueMode"] = val




	# Property definitions:
	Format = property(_getFormat, _setFormat, None,
			_("""Several pre-defined formats are available. When you set the Format
			property, any Mask setting is ignored, and the specified Format is
			used instead. The format codes are NOT case-sensitive.  (str)

			Formats are available in several categories:
				Date (US and European)
				DateTime (US and European)
				Time
				Email
				IP Address
				SSN (US)
				Zip Code (US)
				Phone (US)
				"""))

	InputCodes = property(_getInputCodes, _setInputCodes, None,
			_("""Characters that define the type of input that the control will accept.  (str)

			These are the available input codes and their meaning:

			+-----------+---------------------------------------------------------------+
			|Character  |Meaning                                                        |
			+===========+===============================================================+
			|   #       |Allow numeric only (0-9)                                       |
			+-----------+---------------------------------------------------------------+
			|   _       |Allow spaces                                                   |
			+-----------+---------------------------------------------------------------+
			|   !       |Force upper                                                    |
			+-----------+---------------------------------------------------------------+
			|   ^       |Force lower                                                    |
			+-----------+---------------------------------------------------------------+
			|   R       |Right-align field(s)                                           |
			+-----------+---------------------------------------------------------------+
			|   r       |Right-insert in field(s) (implies R)                           |
			+-----------+---------------------------------------------------------------+
			|   <       |Stay in field until explicit navigation out of it              |
			+-----------+---------------------------------------------------------------+
			|   >       |Allow insert/delete within partially filled fields (as         |
			|           |opposed to the default "overwrite" mode for fixed-width        |
			|           |masked edit controls.)  This allows single-field controls      |
			|           |or each field within a multi-field control to optionally       |
			|           |behave more like standard text controls.                       |
			|           |(See EMAIL or phone number autoformat examples.)               |
			|           |                                                               |
			|           |Note: This also governs whether backspace/delete operations    |
			|           |shift contents of field to right of cursor, or just blank the  |
			|           |erased section.                                                |
			|           |                                                               |
			|           |Also, when combined with 'r', this indicates that the field    |
			|           |or control allows right insert anywhere within the current     |
			|           |non-empty value in the field.(Otherwise right-insert behavior  |
			|           |is only performed to when the entire right-insertable field    |
			|           |is selected or the cursor is at the right edge of the field.   |
			+-----------+---------------------------------------------------------------+
			|   ,       |Allow grouping character in integer fields of numeric controls |
			|           |and auto-group/regroup digits (if the result fits) when leaving|
			|           |such a field.  (If specified, .SetValue() will attempt to      |
			|           |auto-group as well.)                                           |
			|           |',' is also the default grouping character.  To change the     |
			|           |grouping character and/or decimal character, use the groupChar |
			|           |and decimalChar parameters, respectively.                      |
			|           |                                                               |
			|           |Note: typing the "decimal point" character in such fields will |
			|           |clip the value to that left of the cursor for integer          |
			|           |fields of controls with "integer" or "floating point" masks.   |
			|           |If the ',' format code is specified, this will also cause the  |
			|           |resulting digits to be regrouped properly, using the current   |
			|           |grouping character.                                            |
			+-----------+---------------------------------------------------------------+
			|   -       |Prepend and reserve leading space for sign to mask and allow   |
			|           |signed values (negative #s shown in red by default.) Can be    |
			|           |used with argument useParensForNegatives (see below.)          |
			+-----------+---------------------------------------------------------------+
			|   0       |integer fields get leading zeros                               |
			+-----------+---------------------------------------------------------------+
			|   D       |Date[/time] field                                              |
			+-----------+---------------------------------------------------------------+
			|   T       |Time field                                                     |
			+-----------+---------------------------------------------------------------+
			|   F       |Auto-Fit: the control calulates its size from                  |
			|           |the length of the template mask                                |
			+-----------+---------------------------------------------------------------+
			|   V       |validate entered chars against validRegex before allowing them |
			|           |to be entered vs. being allowed by basic mask and then having  |
			|           |the resulting value just colored as invalid.                   |
			|           |(See USSTATE autoformat demo for how this can be used.)        |
			+-----------+---------------------------------------------------------------+
			|   S       |select entire field when navigating to new field               |
			+-----------+---------------------------------------------------------------+


			"""))

	Mask = property(_getMask, _setMask, None,
			_("""Display Mask for the control.  (str)

			These are the allowed mask characters and their function:

			+-----------+-------------------------------------------------------------------+
			|Character  |Function                                                           +
			+===========+===================================================================+
			|   #       |Allow numeric only (0-9)                                           |
			+-----------+-------------------------------------------------------------------+
			|   N       |Allow letters and numbers (0-9)                                    |
			+-----------+-------------------------------------------------------------------+
			|   A       |Allow uppercase letters only                                       |
			+-----------+-------------------------------------------------------------------+
			|   a       |Allow lowercase letters only                                       |
			+-----------+-------------------------------------------------------------------+
			|   C       |Allow any letter, upper or lower                                   |
			+-----------+-------------------------------------------------------------------+
			|   X       |Allow string.letters, string.punctuation, string.digits            |
			+-----------+-------------------------------------------------------------------+
			|   &       |Allow string.punctuation only (doesn't include all unicode symbols)|
			+-----------+-------------------------------------------------------------------+
			|   \*      |Allow any visible character                                        |
			+-----------+-------------------------------------------------------------------+
			|   |       |explicit field boundary (takes no space in the control; allows mix |
			|           |of adjacent mask characters to be treated as separate fields,      |
			|           |eg: '&|###' means "field 0 = '&', field 1 = '###'", but there's    |
			|           |no fixed characters in between.                                    |
			+-----------+-------------------------------------------------------------------+

			Repetitions of the same mask code can be represented by placing the number
			of repetitions in curly braces after the code. E.g.: CCCCCCCC = C{6} """))

	MaskedValue = property(_getMaskedValue, None, None,
			_("Value of the control, including mask characters, if any. (read-only) (str)"))

	UnmaskedValue = property(_getUnmaskedValue, None, None,
			_("Value of the control, removing mask characters, if any. (read-only) (str)"))

	Value = property(_getValue, _setValue, None,
			_("""Specifies the content of this control. (str) If ValueMode is set to 'Masked',
			this will include the mask characters. Otherwise it will be the contents without
			any mask characters."""))

	ValueMode = property(_getValueMode, _setValueMode, None,
			_("""Specifies the information that the Value property refers to. (str)
			If it is set to 'Masked' (or anything that begins with the letter 'm'), the
			Value property will return the contents of the control, including any mask
			characters. If this is set to anything other than a string that begins with 'm',
			Value will return the control's contents without the mask characters.
			NOTE: This only affects the results of \*reading\* the Value property. Setting
			Value is not affected in any way."""))

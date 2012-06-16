import os
import re
import hashlib
import Cookie
from datetime import datetime
from datetime import timedelta


def encrypt(plaintext, salt="", sha="512"):
    """ Returns the encrypted hexdigest of a plaintext and salt"""

    if sha == "1":
        phrase = hashlib.sha1()
    elif sha == "256":
        phrase = hashlib.sha256()
    else:
        phrase = hashlib.sha512()
    phrase.update("%s@%s" % (plaintext, salt))
    return phrase.hexdigest()


def write_cookie(cls, COOKIE_NAME, COOKIE_VALUE, path, expires=7200):
    """
    Write a cookie
    @path = could be a cls.request.path to set a specific path
    @expires = seconds (integer) to expire the cookie, by default 2 hours ()
    expires = 7200 # 2 hours
    expires = 1209600 # 2 weeks
    expires = 2629743 # 1 month
    """

    # days, seconds, then other fields.
    time_expire = datetime.now() + timedelta(seconds=expires)
    time_expire = time_expire.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    cls.response.headers.add_header(
        'Set-Cookie', COOKIE_NAME+'='+COOKIE_VALUE+'; expires='+str(time_expire)+'; path='+path+'; HttpOnly')
    return


def read_cookie(cls, name):
    """
    Use: cook.read(cls, COOKIE_NAME)
    """

    string_cookie = os.environ.get('HTTP_COOKIE', '')
    cls.cookie = Cookie.SimpleCookie()
    cls.cookie.load(string_cookie)
    value = None
    if cls.cookie.get(name):
        value  = cls.cookie[name].value

    return value


def get_date_time(format="%Y-%m-%d %H:%M:%S", UTC_OFFSET=3):
    """
    Get date and time in UTC for Chile with a specific format
    """

    local_datetime = datetime.now()
    now = local_datetime - timedelta(hours=UTC_OFFSET)
    if format != "datetimeProperty":
        now = now.strftime(format)
    #    now = datetime.fromtimestamp(1321925140.78)
    return now

EMAIL_REGEXP = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"

def is_email_valid(email):
    if len(email) > 7:
        if re.match(EMAIL_REGEXP, email) != None:
            return 1
    return 0

ALPHANUMERIC_REGEXP = "^\w+$"

def is_alphanumeric(field):
    if re.match(ALPHANUMERIC_REGEXP, field) is not None:
        return 1
    return 0


def get_device(cls):
    uastring = cls.request.user_agent
    is_mobile = (("Mobile" in uastring and "Safari" in uastring) or \
	 ("Windows Phone OS" in uastring and "IEMobile" in uastring) or \
     ("Blackberry") in uastring)

    if "MSIE" in uastring:
        browser = "Explorer"
    elif "Firefox" in uastring:
        browser = "Firefox"
    elif "Presto" in uastring:
        browser = "Opera"
    elif "Android" in uastring and "AppleWebKit" in uastring:
        browser = "Chrome for andriod"
    elif "iPhone" in uastring and "AppleWebKit" in uastring:
        browser = "Safari for iPhone"
    elif "iPod" in uastring and "AppleWebKit" in uastring:
        browser = "Safari for iPod"
    elif "iPad" in uastring and "AppleWebKit" in uastring:
        browser = "Safari for iPad"
    elif "Chrome" in uastring:
        browser = "Chrome"
    elif "AppleWebKit" in uastring:
        browser = "Safari"
    else:
        browser = "unknown"

    device = {
        "is_mobile": is_mobile,
        "browser": browser,
        "uastring": uastring
    }

    return device


def set_device_cookie_and_return_bool(cls, force=""):
    """
    set a cookie for device (dvc) returning a dict and set cookie
    Cookie value has to be "mobile" or "desktop" string
    """
    if force != "":
        # force cookie to param
        device_cookie = force
    elif cls.request.get("device") == "":
        # ask for cookie of device
        device_cookie = str(read_cookie(cls, "dvc"))
        if not device_cookie or device_cookie == "None" or device_cookie == "":
            # If cookie has an error, check which device is been used
            if get_device(cls)["is_mobile"]:
                device_cookie = "mobile"
            else:
                device_cookie = "desktop"
    else:
        # set cookie to param 'is_mobile' value directly
        device_cookie = cls.request.get("device")

    # Set Cookie for Two weeks with 'device_cookie' value
    write_cookie(cls, "dvc", str(device_cookie), "/", 1209600)
    return device_cookie == "mobile"

COUNTRIES = [
    ("None", "Country..."),
    ("AF", "Afghanistan"),
    ("AL", "Albania"),
    ("DZ", "Algeria"),
    ("AS", "American Samoa"),
    ("AD", "Andorra"),
    ("AG", "Angola"),
    ("AI", "Anguilla"),
    ("AG", "Antigua &amp; Barbuda"),
    ("AR", "Argentina"),
    ("AA", "Armenia"),
    ("AW", "Aruba"),
    ("AU", "Australia"),
    ("AT", "Austria"),
    ("AZ", "Azerbaijan"),
    ("BS", "Bahamas"),
    ("BH", "Bahrain"),
    ("BD", "Bangladesh"),
    ("BB", "Barbados"),
    ("BY", "Belarus"),
    ("BE", "Belgium"),
    ("BZ", "Belize"),
    ("BJ", "Benin"),
    ("BM", "Bermuda"),
    ("BT", "Bhutan"),
    ("BO", "Bolivia"),
    ("BL", "Bonaire"),
    ("BA", "Bosnia &amp; Herzegovina"),
    ("BW", "Botswana"),
    ("BR", "Brazil"),
    ("BC", "British Indian Ocean Ter"),
    ("BN", "Brunei"),
    ("BG", "Bulgaria"),
    ("BF", "Burkina Faso"),
    ("BI", "Burundi"),
    ("KH", "Cambodia"),
    ("CM", "Cameroon"),
    ("CA", "Canada"),
    ("IC", "Canary Islands"),
    ("CV", "Cape Verde"),
    ("KY", "Cayman Islands"),
    ("CF", "Central African Republic"),
    ("TD", "Chad"),
    ("CD", "Channel Islands"),
    ("CL", "Chile"),
    ("CN", "China"),
    ("CI", "Christmas Island"),
    ("CS", "Cocos Island"),
    ("CO", "Colombia"),
    ("CC", "Comoros"),
    ("CG", "Congo"),
    ("CK", "Cook Islands"),
    ("CR", "Costa Rica"),
    ("CT", "Cote D'Ivoire"),
    ("HR", "Croatia"),
    ("CU", "Cuba"),
    ("CB", "Curacao"),
    ("CY", "Cyprus"),
    ("CZ", "Czech Republic"),
    ("DK", "Denmark"),
    ("DJ", "Djibouti"),
    ("DM", "Dominica"),
    ("DO", "Dominican Republic"),
    ("TM", "East Timor"),
    ("EC", "Ecuador"),
    ("EG", "Egypt"),
    ("SV", "El Salvador"),
    ("GQ", "Equatorial Guinea"),
    ("ER", "Eritrea"),
    ("EE", "Estonia"),
    ("ET", "Ethiopia"),
    ("FA", "Falkland Islands"),
    ("FO", "Faroe Islands"),
    ("FJ", "Fiji"),
    ("FI", "Finland"),
    ("FR", "France"),
    ("GF", "French Guiana"),
    ("PF", "French Polynesia"),
    ("FS", "French Southern Ter"),
    ("GA", "Gabon"),
    ("GM", "Gambia"),
    ("GE", "Georgia"),
    ("DE", "Germany"),
    ("GH", "Ghana"),
    ("GI", "Gibraltar"),
    ("GB", "Great Britain"),
    ("GR", "Greece"),
    ("GL", "Greenland"),
    ("GD", "Grenada"),
    ("GP", "Guadeloupe"),
    ("GU", "Guam"),
    ("GT", "Guatemala"),
    ("GN", "Guinea"),
    ("GY", "Guyana"),
    ("HT", "Haiti"),
    ("HW", "Hawaii"),
    ("HN", "Honduras"),
    ("HK", "Hong Kong"),
    ("HU", "Hungary"),
    ("IS", "Iceland"),
    ("IN", "India"),
    ("ID", "Indonesia"),
    ("IA", "Iran"),
    ("IQ", "Iraq"),
    ("IR", "Ireland"),
    ("IM", "Isle of Man"),
    ("IL", "Israel"),
    ("IT", "Italy"),
    ("JM", "Jamaica"),
    ("JP", "Japan"),
    ("JO", "Jordan"),
    ("KZ", "Kazakhstan"),
    ("KE", "Kenya"),
    ("KI", "Kiribati"),
    ("NK", "Korea North"),
    ("KS", "Korea South"),
    ("KW", "Kuwait"),
    ("KG", "Kyrgyzstan"),
    ("LA", "Laos"),
    ("LV", "Latvia"),
    ("LB", "Lebanon"),
    ("LS", "Lesotho"),
    ("LR", "Liberia"),
    ("LY", "Libya"),
    ("LI", "Liechtenstein"),
    ("LT", "Lithuania"),
    ("LU", "Luxembourg"),
    ("MO", "Macau"),
    ("MK", "Macedonia"),
    ("MG", "Madagascar"),
    ("MY", "Malaysia"),
    ("MW", "Malawi"),
    ("MV", "Maldives"),
    ("ML", "Mali"),
    ("MT", "Malta"),
    ("MH", "Marshall Islands"),
    ("MQ", "Martinique"),
    ("MR", "Mauritania"),
    ("MU", "Mauritius"),
    ("ME", "Mayotte"),
    ("MX", "Mexico"),
    ("MI", "Midway Islands"),
    ("MD", "Moldova"),
    ("MC", "Monaco"),
    ("MN", "Mongolia"),
    ("MS", "Montserrat"),
    ("MA", "Morocco"),
    ("MZ", "Mozambique"),
    ("MM", "Myanmar"),
    ("NA", "Nambia"),
    ("NU", "Nauru"),
    ("NP", "Nepal"),
    ("AN", "Netherland Antilles"),
    ("NL", "Netherlands (Holland, Europe)"),
    ("NV", "Nevis"),
    ("NC", "New Caledonia"),
    ("NZ", "New Zealand"),
    ("NI", "Nicaragua"),
    ("NE", "Niger"),
    ("NG", "Nigeria"),
    ("NW", "Niue"),
    ("NF", "Norfolk Island"),
    ("NO", "Norway"),
    ("OM", "Oman"),
    ("PK", "Pakistan"),
    ("PW", "Palau Island"),
    ("PS", "Palestine"),
    ("PA", "Panama"),
    ("PG", "Papua New Guinea"),
    ("PY", "Paraguay"),
    ("PE", "Peru"),
    ("PH", "Philippines"),
    ("PO", "Pitcairn Island"),
    ("PL", "Poland"),
    ("PT", "Portugal"),
    ("PR", "Puerto Rico"),
    ("QA", "Qatar"),
    ("ME", "Republic of Montenegro"),
    ("RS", "Republic of Serbia"),
    ("RE", "Reunion"),
    ("RO", "Romania"),
    ("RU", "Russia"),
    ("RW", "Rwanda"),
    ("NT", "St Barthelemy"),
    ("EU", "St Eustatius"),
    ("HE", "St Helena"),
    ("KN", "St Kitts-Nevis"),
    ("LC", "St Lucia"),
    ("MB", "St Maarten"),
    ("PM", "St Pierre &amp; Miquelon"),
    ("VC", "St Vincent &amp; Grenadines"),
    ("SP", "Saipan"),
    ("SO", "Samoa"),
    ("AS", "Samoa American"),
    ("SM", "San Marino"),
    ("ST", "Sao Tome &amp; Principe"),
    ("SA", "Saudi Arabia"),
    ("SN", "Senegal"),
    ("SC", "Seychelles"),
    ("SL", "Sierra Leone"),
    ("SG", "Singapore"),
    ("SK", "Slovakia"),
    ("SI", "Slovenia"),
    ("SB", "Solomon Islands"),
    ("OI", "Somalia"),
    ("ZA", "South Africa"),
    ("ES", "Spain"),
    ("LK", "Sri Lanka"),
    ("SD", "Sudan"),
    ("SR", "Suriname"),
    ("SZ", "Swaziland"),
    ("SE", "Sweden"),
    ("CH", "Switzerland"),
    ("SY", "Syria"),
    ("TA", "Tahiti"),
    ("TW", "Taiwan"),
    ("TJ", "Tajikistan"),
    ("TZ", "Tanzania"),
    ("TH", "Thailand"),
    ("TG", "Togo"),
    ("TK", "Tokelau"),
    ("TO", "Tonga"),
    ("TT", "Trinidad &amp; Tobago"),
    ("TN", "Tunisia"),
    ("TR", "Turkey"),
    ("TU", "Turkmenistan"),
    ("TC", "Turks &amp; Caicos Is"),
    ("TV", "Tuvalu"),
    ("UG", "Uganda"),
    ("UA", "Ukraine"),
    ("AE", "United Arab Emirates"),
    ("GB", "United Kingdom"),
    ("US", "United States of America"),
    ("UY", "Uruguay"),
    ("UZ", "Uzbekistan"),
    ("VU", "Vanuatu"),
    ("VS", "Vatican City State"),
    ("VE", "Venezuela"),
    ("VN", "Vietnam"),
    ("VB", "Virgin Islands (Brit)"),
    ("VA", "Virgin Islands (USA)"),
    ("WK", "Wake Island"),
    ("WF", "Wallis &amp; Futana Is"),
    ("YE", "Yemen"),
    ("ZR", "Zaire"),
    ("ZM", "Zambia"),
    ("ZW", "Zimbabwe")]

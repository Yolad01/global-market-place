from decimal import Decimal

from django.db import models


class Currencies(models.TextChoices):
    USD = "USD"  # US Dollar
    AFN = "AFN"  # Afghan Afghani
    DZD = "DZD"  # Algerian Dinar
    ARS = "ARS"  # Argentine Peso
    AMD = "AMD"  # Armenian Dram
    AWG = "AWG"  # Aruban Guilder
    AUD = "AUD"  # Australian Dollar
    AZN = "AZN"  # Azerbaijan Manat
    BSD = "BSD"  # Bahamian Dollar
    BHD = "BHD"  # Bahraini Dinar
    THB = "THB"  # Baht
    PAB = "PAB"  # Balboa
    BBD = "BBD"  # Barbados Dollar
    BYN = "BYN"  # Belarusian Ruble
    BZD = "BZD"  # Belize Dollar
    BMD = "BMD"  # Bermudian Dollar
    BOB = "BOB"  # Boliviano
    VEF = "VEF"  # Bolívar fuerte venezolano
    BRL = "BRL"  # Brazilian Real
    BND = "BND"  # Brunei Dollar
    BGN = "BGN"  # Bulgarian Lev
    BIF = "BIF"  # Burundi Franc
    XOF = "XOF"  # CFA Franc BCEAO
    XAF = "XAF"  # CFA Franc BEAC
    XPF = "XPF"  # CFP Franc
    CAD = "CAD"  # Canadian Dollar
    CVE = "CVE"  # Cape Verde Escudo
    KYD = "KYD"  # Cayman Islands Dollar
    CLP = "CLP"  # Chilean Peso
    COP = "COP"  # Colombian Peso
    KMF = "KMF"  # Comoro Franc
    BAM = "BAM"  # Convertible Mark
    NIO = "NIO"  # Cordoba Oro
    CRC = "CRC"  # Costa Rican Colon
    HRK = "HRK"  # Croatian Kuna
    CYP = "CYP"  # Cypriot Pound
    CZK = "CZK"  # Czech Koruna
    GMD = "GMD"  # Dalasi
    DKK = "DKK"  # Danish Krone
    DJF = "DJF"  # Djibouti Franc
    STD = "STD"  # Dobra
    DOP = "DOP"  # Dominican Peso
    VND = "VND"  # Dong
    XCD = "XCD"  # East Carribbean Dollar
    EGP = "EGP"  # Egyptian Pound
    ETB = "ETB"  # Ethiopian Birr
    EUR = "EUR"  # Euro
    FKP = "FKP"  # Falkland Islands Pound
    FJD = "FJD"  # Fiji Dollar
    HUF = "HUF"  # Forint
    CDF = "CDF"  # Franc Congolais
    GHS = "GHS"  # Ghanaian Cedi
    GIP = "GIP"  # Gibraltar Pound
    HTG = "HTG"  # Gourde
    PYG = "PYG"  # Guarani
    GNF = "GNF"  # Guinea Franc
    GYD = "GYD"  # Guyana Dollar
    HKD = "HKD"  # Hong Kong Dollar
    UAH = "UAH"  # Hryvnia
    ISK = "ISK"  # Iceland Krona
    INR = "INR"  # Indian Rupee
    IQD = "IQD"  # Iraqi Dinar
    ILS = "ILS"  # Israeli New Sheqel
    JMD = "JMD"  # Jamaican Dollar
    JOD = "JOD"  # Jordanian Dinar
    KES = "KES"  # Kenyan Shilling
    PGK = "PGK"  # Kina
    LAK = "LAK"  # Kip
    KRW = "KRW"  # Korean Won
    KWD = "KWD"  # Kuwaiti Dinar
    MWK = "MWK"  # Kwacha
    AOA = "AOA"  # Kwanza
    MMK = "MMK"  # Kyat
    GEL = "GEL"  # Lari
    LBP = "LBP"  # Lebanese Pound
    ALL = "ALL"  # Lek
    HNL = "HNL"  # Lempira
    SLL = "SLL"  # Leone
    LRD = "LRD"  # Liberian Dollar
    LYD = "LYD"  # "Libyan dinar - LYD (ل.د),
    SZL = "SZL"  # Lilangeni
    LSL = "LSL"  # Loti
    MKD = "MKD"  # Macedonian Denar
    MGA = "MGA"  # Malagasy Ariary
    MYR = "MYR"  # Malaysian Ringgit
    MUR = "MUR"  # Mauritius Rupee
    MXN = "MXN"  # Mexican Peso
    MDL = "MDL"  # Moldovan Leu
    MAD = "MAD"  # "Moroccan Dirham - MAD (د.م.)"
    MZN = "MZN"  # Mozambican Metical
    NGN = "NGN"  # Naira
    ERN = "ERN"  # Nakfa
    NAD = "NAD"  # Namibian Dollar
    NPR = "NPR"  # Nepalese Rupee
    ANG = "ANG"  # Netherlands Antillan Guilder
    TWD = "TWD"  # New Taiwan Dollar
    NZD = "NZD"  # New Zealand Dollar
    BTN = "BTN"  # Ngultrum
    NOK = "NOK"  # Norwegian Krone
    PEN = "PEN"  # Nuevo Sol
    MRO = "MRO"  # Ouguiya (UM)
    TOP = "TOP"  # Pa'anga (T$)
    PKR = "PKR"  # "Pakistan Rupee (₨)"
    MOP = "MOP"  # Pataca (MOP$)
    UYU = "UYU"  # "Peso Uruguayo  ($U)",
    PHP = "PHP"  # Philippine Peso  (₱)
    GBP = "GBP"  # Pound Sterling  (£)
    BWP = "BWP"  # Pula
    QAR = "QAR"  # Qatari Rial
    GTQ = "GTQ"  # Quetzal
    ZAR = "ZAR"  # Rand
    OMR = "OMR"  # Rial Omani
    KHR = "KHR"  # Riel
    RON = "RON"  # Romanian Lei
    MVR = "MVR"  # Rufiyaa
    IDR = "IDR"  # Rupiah
    RUB = "RUB"  # Russian Ruble  (руб.)
    RWF = "RWF"  # Rwanda Franc
    SHP = "SHP"  # Saint Helena Pound
    SAR = "SAR"  # Saudi Riyal
    RSD = "RSD"  # Serbian Dinar
    SCR = "SCR"  # Seychelles Rupee
    SGD = "SGD"  # Singapore Dollar
    SBD = "SBD"  # Solomon Islands Dollar
    KGS = "KGS"  # Som
    SOS = "SOS"  # Somali Shilling
    SDG = "SDG"  # Sudanese pounds
    SSP = "SSP"  # South Sudanese pounds
    TJS = "TJS"  # Somoni
    LKR = "LKR"  # Sri Lanka Rupee
    SRD = "SRD"  # Surinamese Dollar
    SEK = "SEK"  # Swedish Krona
    CHF = "CHF"  # Swiss Franc
    BDT = "BDT"  # Taka
    WST = "WST"  # Tala
    TZS = "TZS"  # Tanzanian Shilling
    KZT = "KZT"  # Tenge
    TTD = "TTD"  # Trinidad and Tobago Dollar
    MNT = "MNT"  # Tugrik (Tugrug)
    TND = "TND"  # Tunisian Dinar
    TMT = "TMT"  # Turkmenistani Manat
    TRY = "TRY"  # Türk lirası
    AED = "AED"  # UAE Dirham
    UGX = "UGX"  # Uganda Shilling
    UZS = "UZS"  # Uzbekistan Sum (сум)
    VUV = "VUV"  # Vatu
    YER = "YER"  # "Yemeni Rial - YER (﷼)
    JPY = "JPY"  # Yen
    CNY = "CNY"  # Yuan Renminbi
    ZMW = "ZMW"  # Zambian Kwacha - ZMW
    ZWL = "ZWL"  # Zimbabwean dollar- ZWL
    PLN = "PLN"  # Zloty


# They are not currently in the currency choices {Currency.CLF, Currency.UYW}
FOUR_DECIMAL_CURRENCIES: set[Currencies] = set()

THREE_DECIMAL_CURRENCIES: set[Currencies] = {
    Currencies.BHD,
    Currencies.IQD,
    Currencies.JOD,
    Currencies.KWD,
    Currencies.LYD,
    Currencies.OMR,
    Currencies.TND,
}

ZERO_DECIMAL_CURRENCIES: set[Currencies] = {
    Currencies.BIF,
    Currencies.CLP,
    Currencies.DJF,
    Currencies.GNF,
    Currencies.JPY,
    Currencies.KMF,
    Currencies.KRW,
    Currencies.MGA,
    Currencies.PYG,
    Currencies.RWF,
    Currencies.VND,
    Currencies.VUV,
    Currencies.XAF,
    Currencies.XOF,
    Currencies.XPF,
}


def to_minor_unit(currency: Currencies, value: Decimal) -> int:
    """
    Utility to convert a currency value from its main unit to it's smallest unit.
    E.g. For `Currency.USD` it $10 is converted to 1000 cents equivalent
    :param currency: The currency whose main unit is being converted
    :param value: The decimal value of the currency in its major unit
    :return: The equivalent of the currency value in its smallest unit
    """
    if currency in ZERO_DECIMAL_CURRENCIES:
        minor_unit = int(value)
    elif currency in THREE_DECIMAL_CURRENCIES:
        minor_unit = int(value * 1000)
    elif currency in FOUR_DECIMAL_CURRENCIES:
        minor_unit = int(value * 10_000)
    else:
        minor_unit = int(value * 100)
    return minor_unit


def to_major_unit(currency: Currencies, value: Decimal) -> Decimal:
    """
    Utility to convert a currency value from its smallest unit.
    E.g. For `Currency.USD` it's 1000 cents is converted to $10 equivalent
    :param currency: The currency whose smallest unit is being converted
    :param value: The decimal value of the currency in its major unit
    :return: The equivalent of the currency value in its major unit"""
    if currency in ZERO_DECIMAL_CURRENCIES:
        major_unit = value
    elif currency in THREE_DECIMAL_CURRENCIES:
        major_unit = value / 1000
    elif currency in FOUR_DECIMAL_CURRENCIES:
        major_unit = value / 10_000
    else:
        major_unit = value / 100
    return major_unit

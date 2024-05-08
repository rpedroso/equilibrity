import os
import wx


def get_data_dir():
    """
    Return the standard location on this platform for application data
    """
    sp = wx.StandardPaths.Get()
    return sp.GetUserDataDir()


def exists(filename):
    data_dir = get_data_dir()
    return os.path.exists(os.path.join(data_dir, filename))


def mkdir():
    if not os.path.exists(get_data_dir()):
        os.makedirs(get_data_dir())


def get_config(filename):
    config = wx.FileConfig(
        localFilename=os.path.join(get_data_dir(), filename))
    return config


def get_wallets_dir():
    wallets_dir = os.path.join(get_data_dir(), 'wallets')
    if not os.path.exists(wallets_dir):
        os.makedirs(wallets_dir)
    return wallets_dir


def read_wallet_nettype(cfgobj):
    return cfgobj.ReadInt('wallet/nettype')


def write_wallet_nettype(cfgobj, nettype):
    cfgobj.WriteInt('wallet/nettype', nettype)


def read_wallet_daemon(cfgobj):
    return cfgobj.Read('wallet/daemon')


def write_wallet_daemon(cfgobj, daemon):
    cfgobj.Write('wallet/daemon', daemon)

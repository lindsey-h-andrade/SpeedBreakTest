from splinter import Browser

executable_path = {'executable_path':'</path/to/chrome>'}


b = Browser('chrome', **executable_path)
b.visit('http://cobrateam.info')



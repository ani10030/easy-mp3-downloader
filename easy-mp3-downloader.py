from bs4 import BeautifulSoup	#importing beautifulSoup
import requests
import urllib
import os
import sys
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def title():
	print('')
	print('		-------- EASY MP3 DOWNLOADER --------')
	print('')
	print('')

def main_menu():
	title()
	try:
		print('	---------------')
		print('	|- Main Menu -|')
		print('	---------------')
		print('')
		print('	1. Latest Punjabi Songs')
		print('	2. Latest Hindi Songs')
		print('	3. Latest English Songs')
		print('	4. Exit')
		print('')
		user_choice=int(input('Input Choice = '))
		sub_menu(user_choice)
	except:
		print('')
		print('	-- Please input any one choice from above only--')
		print('')
		enter=raw_input('	Press enter to try again')
		os.system('cls')
		os.system('clear')
		main_menu()

def sub_menu(user_choice):
	os.system('cls')
	os.system('clear')

	if (user_choice==1):
		title()
		print('	------------------------------------')
		print('	|- Latest Punjabi Songs - MP3|320Kbps|')
		print('	------------------------------------')
		print('')
		function_top_punjabi()
	elif (user_choice==2):
		title()
		print('	----------------------------------')
		print('	|- Latest Hindi Songs - MP3|320Kbps|')
		print('	----------------------------------')
		print('')
		obj=Hindi()
		obj.function_top_hindi()
	elif (user_choice==3):
		title()
		print('	------------------------------------')
		print('	|- Latest English Songs - MP3|320Kbps|')
		print('	------------------------------------')
		print('')
		obj=English()
		obj.function_top_english()
	elif (user_choice==4):
		title()
		print('	----------')
		print('	|- Exit -|')
		print('	----------')
		print('')
		function_exit()
	else:
		print('')
		enter=raw_input('	-- Invalid option selected... Press enter to try again --')
		print('')
		main_menu()

def function_top_punjabi():
	try:
		print('-- Please wait while list of top Punjabi songs is getting populated\n')
		time.sleep(.300)

		url="https://djpunjab.com/page/top20.html?download=320&type=week"	#url to the final download page
		data=requests.get(url,verify=False)
		soup_data=BeautifulSoup(data.content)
	
		count=1
		song_name_dict={}
		song_link_dict={}

		print('------------------------------------')
		print('-| Top Punjabi Songs of this week |-')
		print('------------------------------------\n')

		for link in soup_data.find_all('a'):
			download_link=link.get('href')
		
			if '.mp3' in download_link:
				link_dict=download_link.split('/')
				song_name=link_dict[-1][:-19]

				song_link_dict.update({count:download_link})
				song_name_dict.update({count:song_name})

				print(str(count)+'. '+song_name)
				count+=1
				time.sleep(.300)
		i=1
		while (i<count):
			file_download(i,song_name_dict[i],song_link_dict[i])
			i+=1
			time.sleep(.500)
			continue
		
		print('')
		print('-----------------------------------------')
		print('	-- DOWNLOAD COMPLETE --')
		print('-----------------------------------------')
		print('')

		function_exit()
		x=raw_input('Press "Enter" to exit.')

	except:
		connection_error()

class Hindi:
	page_link_list=[]
	def function_top_hindi(self):
		try:
			print('-- Please wait while list of top Hindi songs is getting populated\n')
			time.sleep(.300)

			url="https://djpunjab.com/latest-bollywood-top-songs.html"
			data=requests.get(url,verify=False)
			soup_data=BeautifulSoup(data.content)

			count=1
			song_name_dict={}
			song_id_dict={}

			print('------------------------------------')
			print('-| Top Hindi Songs of this week |-')
			print('------------------------------------\n')

			for link in soup_data.find_all('a'):
				page_url=link.get('href')

				if 'mp3-song' in page_url:
					song_id = page_url.split('-')[-1].strip('.html')
					#Hindi.page_link_list.append("https://djpunjab.com"+page_url)
					song_name_dict.update({count:link.text})
					song_id_dict.update({count:song_id})
					print(str(count)+'. '+link.text)
					count+=1
					time.sleep(.300)

			for x in range(1,count):
				song_url = self.request_song_link(song_id_dict[x])
				file_download(x,song_name_dict[x],song_url)
				time.sleep(.500)

			print('')
			print('-----------------------------------------')
			print('	-- DOWNLOAD COMPLETE --')
			print('-----------------------------------------')
			print('')
	
			function_exit()
			x=raw_input('Press "Enter" to exit.')
		except Exception,e:
			print str(e)
			connection_error()

	def request_song_link(self,song_id):
		page = 'https://www.djpunjab.net/page/direct_url.php?track_id='+song_id
		data=requests.get(page,verify=False)
		soup_data=BeautifulSoup(data.content)
		return soup_data.find(id="textfield6").get('value')

class English():
	song_name_dict={}	
	def function_top_english(self):
		try:
			print('-- Please wait while list of top English songs is getting populated\n')
			time.sleep(.300)

			url="https://m.songslover.club/best-of-the-month.html"	#url to the final download page
			data=requests.get(url,verify=False)
			soup_data=BeautifulSoup(data.content)

			all_links = soup_data.find_all('div',attrs={'class':'post-inner'})
			best_of_links = all_links[0].find_all('a')
			album_url=''
			for link in best_of_links:
				if 'BEST OF' in link.text.upper():
					album_url=link['href']
					break
			if album_url=='':
				connection_error()
				return
			
			songs_page = requests.get(album_url)
			soup_data2 = BeautifulSoup(songs_page.content)

			count=1
			song_link_dict={}

			print('------------------------------------')
			print('-| Top English Songs of this week |-')
			print('------------------------------------\n')
			
			#for name in soup_data.find_all('span'):
			for name in soup_data2.find_all('a'):
				if '.mp3' in name['href']:
					song = name.text.encode('ascii','ignore').replace('  ',' - ').replace('Download ','')
					url = name['href']
					English.song_name_dict.update({count:[song,url]})
					print(str(count)+'. '+song)
					count+=1
					time.sleep(.300)
					if count>30:
						break	
			i=1
			for x in range(1,count):
				file_download(x,English.song_name_dict[x][0],'*')
				time.sleep(.500)

			print('')
			print('-----------------------------------------')
			print('	-- DOWNLOAD COMPLETE --')
			print('-----------------------------------------')
			print('')

			function_exit()
			x=raw_input('Press "Enter" to exit.')
		except Exception,e:
			print str(e)
			connection_error()
		
	def request_song_link(self,count):
		url=English.song_name_dict[count][1]
		return url

def function_exit():
	print('')
	print('	-------------------------------------------')
	print('	Thankyou for choosing EASY MP3 DOWNLOADER !')
	print('')
	print('	Fork Me @ GITHUB => Anirudh Sethi - https://github.com/ani10030/')
	print('	----------------------------------------------------------------')
	print('')

def file_download(count,song_name,download_link):

	try:
		file=open(song_name+'.mp3')
		file.close()
		print ('\n'+'\n'+'  '+str(count)+'. '+song_name+'.mp3')
		print ('		...FILE ALREADY EXISTS...')
		print ('')

	except:
		print ('\n'+'\n'+'  '+str(count)+'. '+song_name+'.mp3')
		print ('		FETCHING '+'"'+song_name+'.mp3'+'"')
		print ('')
		if(download_link=='-'):
			obj=Hindi()
			download_link=obj.request_song_link()
			urllib.urlretrieve(download_link,song_name+".mp3",reporthook=download_percent)

		elif(download_link=='*'):
			obj=English()
			download_link=obj.request_song_link(count)
			urllib.urlretrieve(download_link,song_name+".mp3",reporthook=download_percent)
			
		else:
			urllib.urlretrieve(download_link,song_name+".mp3",reporthook=download_percent)
def connection_error():
	print('')
	print('ERROR : 504 - Connection Time-Out')
	print('---------------------------------')
	print('[-] The link you are trying to access is either not responding or taking too long to respond.')
	print('[-] Please check your internet connection and try again.')
	print('')
	print('')

def download_percent(count, blockSize, totalSize):
  	percent = int(count*blockSize*100/totalSize)
  	if count*blockSize<=totalSize:
  		sys.stdout.write('\t[+] '+str(percent)+'% --> '+ str((count*blockSize)/1024) + " Kb of " + str(int(totalSize)/1024) + " Kb"+" Downloaded\r")
  	else:
  		sys.stdout.write('\t[-] '+str(percent)+'% --> '+ str((totalSize)/1024) + " Kb of " + str(int(totalSize)/1024) + " Kb"+" Downloaded\r")
  	sys.stdout.flush()

abc=main_menu()
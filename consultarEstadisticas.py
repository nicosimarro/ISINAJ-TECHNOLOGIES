#Cargamos 2 datasets
iris = data('iris')
tips = data('tips')

# grafica % tweets positivos

tweets = np.linspace(0,60,256, endpoint = True)
#c, s = np.tweets, np.canciones

#tamaño figura
plt.figure(figsize=(8,6))
plt.plot(x,c, color = "blue", linewidth = 2.5, linestyle="-", label ="tweets")
plt.plot(x,s, color = "green", linewidth = 2.5, linestyle="-", label ="canciones")

#personalizando valores de los ejes
plt.xticks([0,10,20,30,40,50],[r'$ +\0 $', r'$+\10$', r'$+\20$', r'$+\30$', r'$+\40$',r'$+\50$']])
plt.yticks([0,+1],[r'$0$', r'$+1$'])
plt.legend(loc='upper left')

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position(('left'))
ax.spines['left'].set_position(('data',0))

plt.show()
#histograma
iris.head()

#twitter y spotify
twitter = iris[iris.Species == 'tweets']
spotify = iris[iris.Species == 'canciones']

plt.figure(figsize=(10, 8))
n, bins, patches = plt.hist(twitter['Petal.Length'], 12, facecolor='blue', label='tweets')
n, bins, patches = plt.hist(spotify['Petal.Length'], 12, facecolor='green', label='canciones')

plt.legend(loc='top_right')
plt.title('Histograma largo de los tweets')
plt.xlabel('largo del tweet')
plt.ylabel('cuenta largo del tweet')
plt.show()


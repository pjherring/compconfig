alias ls='ls -laG'
alias cl='clear'

export MAGICK_HOME="$HOME/dev/ImageMagick"
export PATH="$PATH:$HOME/bin:$MAGICK_HOME/bin"
export DYLD_LIBRARY_PATH="$MAGICK_HOME/lib/"
export JAVA_HOME=`/usr/libexec/java_home`
export MAVEN_OPTS="-Xmx1024M -XX:MaxPermSize=1024M"
export GRADLE_OPTS="-Xmx512M -XX:MaxPermSize=512M"

D=$'\e[37;40m'
PINK=$'\e[35;40m'
GREEN=$'\e[32;40m'
ORANGE=$'\e[33;40m'

hg_ps1() {
  hg prompt "{${D} on ${PINK}{branch}}{${D} at ${ORANGE}{bookmark}}{${GREEN}{status}}" 2> /dev/null
}

export PS1='\n${PINK}\u ${D}at ${ORANGE}\h ${D}in ${GREEN}\w$(hg_ps1) ${D}\n$ '

set -o vi

placeInBin() {
  ln -s "`pwd`/$(basename $1)" "$HOME/bin/$(basename $1)"
}

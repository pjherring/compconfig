
export MAGICK_HOME="$HOME/dev/ImageMagick"
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced
export DYLD_LIBRARY_PATH="$MAGICK_HOME/lib/"
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_21.jdk/Contents/Home"
export DEFAULT_MAVEN_OPTS="-Xmx512M -XX:MaxPermSize=512M"
export MAVEN_DEBUG_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,address=8000,server=y,suspend=n $DEFAULT_MAVEN_OPTS"
export MAVEN_OPTS=$DEFAULT_MAVEN_OPTS
export GRADLE_OPTS="-Xmx512M -XX:MaxPermSize=512M"
export GRADLE_HOME="$HOME/dev/gradle"
export GROOVY_HOME="$HOME/dev/groovy"
export CATALINA_HOME="$HOME/dev/tomcat"
export PATH="$PATH:$GRADLE_HOME/bin:$GROOVY_HOME/bin:$HOME/bin:/opt/local/bin"
export V6="$HOME/sqsp/v6"

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

mvnSetDefaultOpts() {
  unset MAVEN_OPTS
  export MAVEN_OPTS=$DEFAULT_MAVEN_OPTS
}

mvnSetDebugOpts() {
  unset MAVEN_OPTS
  export MAVEN_OPTS=$MAVEN_DEBUG_OPTS
}

runV6() {
  if [ -z "$1" ]; then
    echo "Which do you want to run, aux-server or site-server?"
  fi

  if [ -n "$2" ]; then
    mvnSetDebugOpts
  else
    mvnSetDefaultOpts
  fi

  cd $V6/$1
  mvn tomcat6:run
}

buildV6() {
  if [ -n "$1" ]; then
    cd $V6/$1
    mvnSetDefaultOpts

    if [ -n "$2" ]; then
      mvn clean install
    else
      mvn install
    fi
  else
    echo "Which project do you want to build?"
    return 1
  fi
}

alias ls='ls -lG'
alias cl='clear'
alias gdvim='git difftool --tool=vimdiff --no-prompt'
alias rabbit-fe='open http://localhost:15672'
alias es-fe='open http://localhost:9200/_plugin/head'
alias build-aux='buildV6 aux-server'
alias build-site='buildV6 site-server'
alias run-aux="runV6 aux-server"
alias debug-aux="runV6 aux-server debug"
alias run-site="runV6 site-server"
alias debug-site="runV6 site-server debug"
alias sqsp-ports="sudo $V6/scripts/bind-osx-ports.sh"
alias v6="cd $V6"

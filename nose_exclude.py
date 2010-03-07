import os
import logging
from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.nose_exclude')

class NoseExclude(Plugin):

    def options(self, parser, env=os.environ):
        """Define the command line options for the plugin."""
        super(NoseExclude, self).options(parser, env)
        parser.add_option(
            "--exclude-dir", action="append",
            dest="exclude_dirs",
            help="Directory to exclude from test discovery. \
                Path can be relative to current working directory \
                or an absolute path. May be specified multiple \
                times. [NOSE_EXCLUDE_DIRS]")
    
    def configure(self, options, conf):
        """Configure plugin based on command line options"""
        super(NoseExclude, self).configure(options, conf)

        self.exclude_dirs = {}

        if not options.exclude_dirs:
            self.enabled = False
            return
        
        self.enabled = True
        root = os.getcwd()
        log.debug('cwd: %s' % root)

        # Normalize excluded directory names for lookup
        for d in options.exclude_dirs:
            if os.path.isabs(d):
                self.exclude_dirs[d] = True
            elif os.path.isdir(d):
                #see if it's relative
                new_abs_d = os.path.join(root,d)
                self.exclude_dirs[new_abs_d] = True
            else:
                #bad path
                raise ValueError("invalid path: %s" % d)

        exclude_str = "excluding dirs: %s" % ",".join(self.exclude_dirs.keys())
        log.debug(exclude_str)

    def wantDirectory(self, dirname):
        """Check if directory is eligible for test discovery"""
        if dirname in self.exclude_dirs:
            log.debug("excluded: %s" % dirname)
            return False
        else:
            return True



            
